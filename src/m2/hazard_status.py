STATUS_PRIORITY = {
    "SAFE": 0,
    "RESTRICTED": 1,
    "BLOCKED": 2
}


def normalize_status(status):
    """
    Convert a status to the supported uppercase form.
    """

    if status is None:
        return "SAFE"

    status = str(status).upper()

    if status not in STATUS_PRIORITY:
        raise ValueError(
            f"Invalid road status: {status}"
        )

    return status


def combine_statuses(*statuses):
    """
    Calculate the effective road status from
    multiple hazard/status sources.

    Priority:

        BLOCKED > RESTRICTED > SAFE
    """

    normalized = [
        normalize_status(status)
        for status in statuses
    ]

    if not normalized:
        return "SAFE"

    return max(
        normalized,
        key=lambda status:
            STATUS_PRIORITY[status]
    )


def calculate_effective_status(
    base_status="SAFE",
    flood_status="SAFE",
    cyclone_status="SAFE"
):
    """
    Calculate the final road status used by routing.

    The strongest restriction among the supplied
    statuses becomes the effective status.
    """

    return combine_statuses(
        base_status,
        flood_status,
        cyclone_status
    )