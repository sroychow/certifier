import os
import re
import tempfile
import logging
from abc import abstractclassmethod
import subprocess
import paramiko
from ckeditor.fields import RichTextField
from decouple import config
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from remotescripts.validators import (
    validate_bash_script,
    validate_comma_space_separated_values_string,
)
from model_utils.managers import InheritanceManager


logger = logging.getLogger(__name__)


class ScriptConfigurationBase(models.Model):
    """
    Base model for configuration common across different
    type of scripts to execute
    """

    objects = InheritanceManager()
    title = models.CharField(
        max_length=50, help_text="Script title to display", null=True
    )

    base_command = models.TextField(
        max_length=500,
        help_text="Base command to run",
        null=False,
        validators=[validate_bash_script],
    )
    show_stdout = models.BooleanField(help_text="Show stdout", default=True)
    show_stderr = models.BooleanField(help_text="Show stderr", default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    help_text = RichTextField(
        max_length=1000,
        help_text="Help text/instructions for users",
        default="",
        null=True,
        blank=True,
    )

    is_running = models.BooleanField(
        help_text="Flag set to True while the script is executing", default=False
    )

    def _form_command(self, *args, **kwargs) -> str:
        """
        Building on the base command, add positional and keyword arguments
        and return the complete command string to execute
        """
        cmd = str(self.base_command)
        num_pos_args = self.positional_arguments.count()
        num_kw_args = self.keyword_arguments.count()
        if num_pos_args > 0:
            if len(args) != num_pos_args:
                raise TypeError(
                    f"Script requires {num_pos_args} positional argument(s) but {len(args)} was given"
                )
            p = self.positional_arguments.filter().order_by("position")

            for i, _p in enumerate(p):
                # TODO Typecheck
                cmd += f" {str(args[i])}"

        if num_kw_args > 0:
            if len(kwargs) != num_kw_args:
                raise TypeError(
                    f"Script requires {num_kw_args} keyword argument(s) but {len(kwargs)} was given"
                )
            k = self.keyword_arguments.all()
            for _k in k:
                if _k.keyword not in kwargs:
                    raise TypeError(f"Missing keyword argument '{_k.keyword}'")
                cmd += f" {str(_k)}{kwargs[_k.keyword]}"
        return cmd

    def save(self, *args, **kwargs):
        """
        Override the save method so that we replace carriage returns
        which are invalid for bash scripts.
        """
        self.base_command = str(self.base_command).replace("\r", "")
        super().save(*args, **kwargs)

    def before_execution(self):
        self.is_running = True
        logger.debug(f"Marking script {self} as running")
        self.save()

    def after_execution(self):
        logger.debug(f"Marking script {self} as not running")
        self.is_running = False
        self.save()

    @abstractclassmethod
    def execute_core(self, *args, **kwargs):
        """
        Abstract class method to be overriden by subclasses.
        Executes the script specified by this instance.
        """

    def execute(self, *args, **kwargs):
        """
        Main script execution.
        Meant to be run in a thread.
        """
        if self.is_running:
            logger.warning("{self} is already running!")
            return

        self.before_execution()
        try:
            self.execute_core(*args, **kwargs)
        except Exception as e:
            logger.error(e)
        self.after_execution()

    @abstractclassmethod
    def get_output(self, *args, **kwargs):
        """
        Abstract class method to be overriden by subclasses.
        Fetches the output files related to the execution of
        the script specified by this instance.
        """
        pass

    class Meta:
        ordering = ["id"]


class BashScriptConfiguration(ScriptConfigurationBase):
    """
    Model for local bash script configuration
    """

    def execute_core(self, *args, **kwargs):
        """
        The idea here is to save the script in a temp file,
        then pass it to bash via subprocess.

        Not tested a lot, but the main idea works.
        """

        cmd_to_execute = self._form_command(*args, **kwargs)
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(cmd_to_execute.encode())
            with subprocess.Popen(["bash", fp.name], stdout=subprocess.PIPE) as process:
                output, error = process.communicate()
            logger.info(output)

    def __str__(self) -> str:
        return f"{self.title} (Local)"


class RemoteScriptConfiguration(ScriptConfigurationBase):
    """
    Model storing configuration for executing scripts on remote hosts
    """

    CONNECTION_SSH_KB = "ssh_kb"
    CONNECTION_PROTOCOL_CHOICES = [(CONNECTION_SSH_KB, "SSH - keyboard interactive")]

    host = models.CharField(
        max_length=50,
        help_text="Remote host to run the command on",
        null=False,
        blank=False,
    )
    port = models.PositiveIntegerField(
        validators=[MaxValueValidator(limit_value=65535)],
        help_text="Remote host port to connect to",
        null=True,
        default=22,
    )
    connection_protocol = models.CharField(
        max_length=10,
        choices=CONNECTION_PROTOCOL_CHOICES,
        help_text="Connection protocol to use",
        default=CONNECTION_SSH_KB,
    )
    env_secret_username = models.CharField(
        max_length=20,
        help_text="Environment variable name where username is stored",
        null=True,
    )
    env_secret_password = models.CharField(
        max_length=20,
        help_text="Environment variable name where password is stored",
        null=True,
    )

    def _configure_callbacks(self, kwargs):
        """
        Externally configurable callbacks to run
        during execute(). Mostly for printing info.
        """
        ATTR_LIST = [
            "on_script_start",
            "on_script_end",
            "on_connect_success",
            "on_connect_failure",
            "on_new_output_line",
            "on_new_output_file",
        ]

        for k in ATTR_LIST:
            if not hasattr(self, k):
                setattr(self, k, lambda: None)
            if k in kwargs:
                var = kwargs.pop(k)
                if callable(var):
                    setattr(self, k, var)

    @staticmethod
    def _line_buffered(f):
        while not f.channel.exit_status_ready():
            for line in f:
                yield line

    def execute_core(self, *args, **kwargs) -> int:
        """
        Method that executes the remote script.
        """
        self._configure_callbacks(kwargs)

        self.on_script_start()
        cmd_to_execute = self._form_command(*args, **kwargs)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                self.host,
                username=config(self.env_secret_username),
                password=config(self.env_secret_password),
                port=self.port,
            )
            self.on_connect_success(self.host)
        except Exception as e:
            # Run function configured externally
            self.on_connect_failure(e)
            raise

        logger.debug(f"Executing '{cmd_to_execute}'")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            cmd_to_execute, get_pty=True
        )

        for line in self._line_buffered(ssh_stdout):
            # Run function configured externally
            self.on_new_output_line(line)
            logger.debug(line)

        exit_status = ssh_stdout.channel.recv_exit_status()
        self.on_script_end(exit_status)
        if exit_status:
            logger.warning(f"Remote process exited with status {exit_status}")
        else:
            logger.info("Remote process terminated with no errors")

            # Handle output files - TODO: put in a method
            output_files = []
            # Need ssh, args, self
            if self.output_files.all().count() > 0:
                logger.info("Fetching output files")
                ftp = ssh.open_sftp()
                # Try to find expected output files
                for f in self.output_files.all():
                    for ff in ftp.listdir(f.directory):
                        logger.debug(f"Checking file '{ff}'")
                        r = re.search(f.filename_regex, ff)
                        if r:
                            logger.debug(f"Matched regex {f.filename_regex}")
                            valid_file = True
                            for k, v in r.groupdict().items():
                                # Expect 'arg' capture groups to match args used
                                # to run execute()
                                if k.startswith("arg"):
                                    pos = int(k[3:]) - 1  # 0-indexed array
                                    if v == args[pos]:
                                        logger.debug(
                                            f"Validated {k} argument (value = {v})"
                                        )
                                    else:
                                        msg = f"Could not validate '{k}' argument. Expected {args[pos]}, got {v}"
                                        logger.error(msg)
                                        valid_file = False
                                        continue

                                elif k in list(
                                    self.keyword_arguments.all().values_list("keyword")
                                ):
                                    logger.debug(
                                        f"Validated '{k}' keyword argument (value = {v})"
                                    )
                                    # TODO
                            if valid_file:
                                logger.info(f"Found output file '{ff}'")
                                output_files.append((f, ff))
                            else:
                                logger.debug(f"Skipping non-matching file")
                    if len(output_files) < 1:
                        raise Exception(
                            f"No files matching regex '{f.filename_regex}' found"
                        )

                # Get output files from remote machine
                for f_db, f_remote in output_files:
                    localpath = os.path.join(tempfile.gettempdir(), f_remote)
                    remotepath = os.path.join(f_db.directory, f_remote)
                    logger.info(f"Copying remote file '{remotepath}' to '{localpath}'")
                    ftp.get(
                        remotepath=remotepath,
                        localpath=localpath,
                    )
                    self.on_new_output_file(f_db.id, localpath)
                ftp.close()
        ssh.close()
        return exit_status

    def __str__(self) -> str:
        return f"{self.title}"


class ScriptOutputFile(models.Model):
    """
    Model representing a file output of a remote script
    """

    mother_script = models.ForeignKey(
        ScriptConfigurationBase,
        on_delete=models.CASCADE,
        help_text="Script instance this file is generated from",
        null=False,
        related_name="output_files",
    )
    directory = models.CharField(
        max_length=255,
        help_text="Directory where the output file is to be found",
        default="~",
    )
    filename_regex = models.CharField(
        max_length=100,
        help_text="Regex to use in directory to find the file",
        validators=[RegexValidator],
        null=False,
    )
    description = models.CharField(
        max_length=100,
        help_text="Output file description",
        null=True,
        default="",
        blank=True,
    )

    def __str__(self):
        return self.filename_regex


class ScriptArgumentBase(models.Model):
    """
    Base model for ScriptConfigurationBase arguments
    """

    ARGUMENT_INT = "INT"  # Integer
    ARGUMENT_STR = "STR"  # String
    ARGUMENT_CHO = "CHO"  # List of choices

    ARGUMENT_CHOICES = (
        (ARGUMENT_INT, "Integer"),
        (ARGUMENT_STR, "String"),
        (ARGUMENT_CHO, "Choices"),
    )
    name = models.CharField(max_length=20, null=True, default="")
    type = models.CharField(
        max_length=3, choices=ARGUMENT_CHOICES, default=ARGUMENT_STR
    )
    valid_choices = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="",
        help_text="A comma separated list of values that the argument will be limited to (Only valid if Type is 'Choices')",
    )

    default_value = models.CharField(
        max_length=50,
        help_text="Default value for this argument",
        null=True,
        blank=True,
    )
    help_text = models.CharField(
        max_length=100,
        help_text="Help related to this argument",
        null=True,
        default="",
        blank=True,
    )

    def clean(self):
        if self.type == self.ARGUMENT_CHO:
            values = validate_comma_space_separated_values_string(self.valid_choices)
            # Validate default value
            if self.default_value and self.default_value not in values:
                raise ValidationError(f"{self.default_value} not found in {values}")
        elif self.type == self.ARGUMENT_INT:
            if self.default_value:
                try:
                    int(self.default_value)
                except ValueError as e:
                    raise ValidationError(f"{self.default_value} is not an int") from e

        super().clean()

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class ScriptPositionalArgument(ScriptArgumentBase):
    """
    Positional argument for a ScriptConfigurationBase instance
    """

    position = models.PositiveSmallIntegerField(
        help_text="Position to be placed after command.",
        validators=[MinValueValidator(limit_value=1)],
    )
    mother_script = models.ForeignKey(
        ScriptConfigurationBase,
        on_delete=models.CASCADE,
        help_text="Script instance this argument applies to",
        null=False,
        related_name="positional_arguments",
    )

    class Meta:
        unique_together = [["position", "mother_script"]]

    def __str__(self):
        return (
            f"{self.name} (Pos:{self.position}) for "
            f"{ScriptConfigurationBase.objects.get_subclass(id=self.mother_script.pk)}"
        )


class ScriptKeywordArgument(ScriptArgumentBase):
    """
    Keyword argument for a ScriptConfigurationBase instance
    """

    SEPARATOR_SPACE = " "
    SEPARATOR_EQUALS = "="
    SEPARATOR_CHOICES = ((SEPARATOR_SPACE, "Space"), (SEPARATOR_EQUALS, "="))
    keyword = models.CharField(
        max_length=50,
        help_text="Keyword name for this argument",
        null=False,
        default="keyword",
    )
    separator = models.CharField(
        max_length=2,
        help_text="Separator between they keyword name and the argument",
        choices=SEPARATOR_CHOICES,
        default=SEPARATOR_SPACE,
    )
    mother_script = models.ForeignKey(
        ScriptConfigurationBase,
        on_delete=models.CASCADE,
        help_text="Script instance this argument applies to",
        null=False,
        related_name="keyword_arguments",
    )

    def __str__(self):
        return f"--{self.keyword}{self.separator}"
