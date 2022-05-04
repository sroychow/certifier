import logging
from xml.etree.ElementTree import ParseError
from requests.exceptions import SSLError, ConnectionError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, JsonResponse
from certifier.forms import CertifyFormWithChecklistForm, BadReasonForm
from certifier.models import TrackerCertification, RunReconstruction, Dataset, BadReason
from certifier.api.serializers import RunReferenceRunSerializer
from openruns.models import OpenRuns
from oms.utils import (
    retrieve_run,
    retrieve_dataset,
    retrieve_dataset_by_reco,
    get_reco_from_dataset,
)
from oms.models import OmsRun
from users.models import User

logger = logging.getLogger(__name__)


@login_required
def addBadReason(request):
    # if this is a POST request we need to process the form data
    form = BadReasonForm()

    return render(request, "certifier/badreason.html", {"form": form})


@login_required
def promoteToReference(request, run_number, reco):
    """
    View which is called from the Shift Leader View, to promote a specific run 
    reconstruction to a reference one.
    """
    try:
        runReconstruction = RunReconstruction.objects.get(
            run__run_number=run_number, reconstruction=reco
        )
    except RunReconstruction.DoesNotExist as run_reco_does_not_exist:
        raise Http404(
            f"The run {run_number} doesn't exist"
        ) from run_reco_does_not_exist

    if request.method == "POST":
        runReconstruction.promote_to_reference()
        return HttpResponseRedirect("/shiftleader/")

    return render(
        request, "certifier/promote.html", {"runReconstruction": runReconstruction}
    )


@login_required
def certify(request, run_number, reconstruction_type=None):

    logger.debug(
        f"Requesting certification of run {run_number} {reconstruction_type if reconstruction_type else ''}"
    )

    # Check if specific combination can be certified by current user
    if not TrackerCertification.can_be_certified_by_user(
        run_number, reconstruction_type, request.user
    ):
        msg = f"Reconstruction {run_number} {reconstruction_type} is already certified by another user"
        logger.warning(msg)
        return render(
            request,
            "certifier/http_error.html",
            context={"error_num": 400, "message": msg},
            status=400,
        )

    dataset = request.GET.get("dataset", None)
    run = None
    try:
        run = retrieve_run(run_number)
        if not dataset:
            if not reconstruction_type:
                dataset = retrieve_dataset(run_number)
            else:
                dataset = retrieve_dataset_by_reco(run_number, reconstruction_type)

    except IndexError as e:
        context = {"message": f"Run {run_number} does not exist"}
        logger.error(f"{context['message']} ({repr(e)})")
        return render(request, "certifier/404.html", context, status=404)
    except (ConnectionError, ParseError,) as e:
        if isinstance(e, ConnectionError):
            msg = "Unable to connect to external API."
        elif isinstance(e, ParseError):
            msg = "CERN authentication failed."
        msg += f" Please proceed to enter the data manually (Error: {e})"
        logger.warning(msg)

        # If no reconstruction is specified and there's no connection
        # to RR, we cannot get the next available reconstruction type & dataset
        if not reconstruction_type:
            context = {
                "message": f"Cannot proceed with certification if no reconstuction type is specified ({e})",
                "error_num": 400,
            }
            return render(request, "certifier/http_error.html", context, status=400)
        # Proceed with warning
        else:
            messages.warning(request, msg)

    except Exception as e:
        context = {"message": e, "error_num": 500}
        logger.exception(repr(e))
        return render(request, "certifier/http_error.html", context, status=500)

    if not reconstruction_type:
        if dataset:
            reconstruction_type = get_reco_from_dataset(dataset)
        else:
            reconstruction_type = None

    # if this is a POST request we need to process the form data
    if request.method == "POST":

        # Add bad reason
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            name = request.POST.get("name", None)
            dataset = request.POST.get("dataset", None)
            description = request.POST.get("description", None)
            run = OmsRun.objects.get(run_number=run_number)

            if name and description and dataset:
                try:
                    BadReason.objects.get(name=name)
                except BadReason.DoesNotExist:
                    BadReason.objects.create(name=name, description=description)

                form = CertifyFormWithChecklistForm()

                context = {
                    "run_number": run_number,
                    "reconstruction_type": reconstruction_type,
                    "run": run,
                    "dataset": dataset,
                    "form": form,
                }

                return render(request, "certifier/certify.html", context)

        try:
            runReconstruction = RunReconstruction.objects.get(
                run__run_number=run_number, reconstruction=reconstruction_type
            )
        except RunReconstruction.DoesNotExist:
            runReconstruction = RunReconstruction.objects.create(
                run=run, reconstruction=reconstruction_type
            )

        dataset, _ = Dataset.objects.get_or_create(dataset=dataset)

        user = User.objects.get(pk=request.user.id)

        # create a form instance and populate it with data from the request:
        form = CertifyFormWithChecklistForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            try:
                trackerCertification = TrackerCertification.objects.get(
                    runreconstruction=runReconstruction
                )
                messages.warning(
                    request,
                    f"Certification for {trackerCertification.runreconstruction.run.run_number} {trackerCertification.runreconstruction.reconstruction} already exists",
                )
            except TrackerCertification.DoesNotExist:
                formToSave = form.save(commit=False)
                formToSave.runreconstruction = runReconstruction
                formToSave.dataset = dataset
                formToSave.user = user
                formToSave.save()
                form.save_m2m()
                messages.info(
                    request,
                    f"Certification for {trackerCertification.runreconstruction.run.run_number} {trackerCertification.runreconstruction.reconstruction} successfully saved",
                )
            return redirect("openruns:openruns")

    # If a GET, we'll create a blank form
    elif request.method == "GET":
        # From openruns colored boxes

        # Default behavior
        form = CertifyFormWithChecklistForm()

    context = {
        "run_number": run_number,
        "reconstruction_type": reconstruction_type,
        "run": run,
        "dataset": dataset,
        "form": form,
    }

    return render(request, "certifier/certify.html", context)


def runRefRun_list(request):
    """
    Simple list view of serialized Reference runs

    Transferred from old 'mldatasets' app
    """
    if request.method == "GET":
        runRefRunsAll = TrackerCertification.objects.all()
        serializer = RunReferenceRunSerializer(runRefRunsAll, many=True)
        return JsonResponse(serializer.data, safe=False)
