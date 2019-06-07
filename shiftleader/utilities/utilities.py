from django.utils import timezone
import datetime

def to_date(date, formatstring="%Y-%m-%d"):
    if isinstance(date, datetime.datetime):
        return date.date()
    if isinstance(date, datetime.date):
        return date
    return datetime.datetime.strptime(date, formatstring).date()

def to_weekdayname(date, formatstring="%Y-%m-%d"):
    return to_date(date, formatstring).strftime("%A")

def get_this_week_filter_parameter():
    start_of_week = timezone.now() - timezone.timedelta(timezone.now().weekday())
    end_of_week = start_of_week + timezone.timedelta(6)

    date_gte = (
        str(start_of_week.year)
        + "-"
        + str(start_of_week.month)
        + "-"
        + str(start_of_week.day)
    )
    date_lte = (
        str(end_of_week.year)
        + "-"
        + str(end_of_week.month)
        + "-"
        + str(end_of_week.day)
    )

    get_parameters = "?date__gte=" + str(date_gte)
    get_parameters += "&date__lte=" + str(date_lte)

    return get_parameters

def convert_run_registry_to_trackercertification(list_of_dictionaries):
    """
    Converts the list of JSON dictionaries into a RunInfo compatible format, i.e.:
    run_class => type__runtype
    dataset => type__dataset

    :param list_of_dictionaries:
    :return:
    """
    for entry in list_of_dictionaries:
        run_class = entry.pop("run_class").lower()
        entry["dataset"] = entry.pop("dataset")
        dataset = entry["dataset"].lower()
        entry["runreconstruction__run__run_number"] = entry.pop("run_number")

        if "collision" in run_class:
            entry["runreconstruction__run__run_type"] = "Collisions"
        elif "cosmic" in run_class:
            entry["runreconstruction__run__run_type"] = "Cosmics"
        elif "collision" in dataset:  # When run_class is e.g. Commissioning18
            entry["runreconstruction__run__run_type"] = "Collisions"
        elif "cosmic" in dataset:
            entry["runreconstruction__run__run_type"] = "Cosmics"

        if "express" in dataset:
            entry["runreconstruction__reconstruction"] = "Express"
        elif "prompt" in dataset:
            entry["runreconstruction__reconstruction"] = "Prompt"
        elif "rereco" in dataset:
            entry["runreconstruction__reconstruction"] = "ReReco"

        entry["pixel"] = entry["pixel"].title()
        entry["strip"] = entry["sistrip"].title()
        entry["tracking"] = entry["tracking"].title()
        entry["strip_lowstat"] = entry.pop("sistrip_lowstat")

    return list_of_dictionaries


def chunks(elements_list, n):
    """
    Split a list into sublists of fixed length n

    Credit: https://stackoverflow.com/a/312464/9907540

    :param elements_list: list of elements that needs to be split
    :param n: chunk size of new lists
    """
    for index in range(0, len(elements_list), n):
        yield elements_list[index : index + n]
