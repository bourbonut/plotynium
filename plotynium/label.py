def reduce(labels: list[str | None]) -> str | None:
    """
    Reduces a list of labels into an unique one by checking consistency between
    labels. For instance, if there are different labels, the function will return
    `None`. However, if only the same label in the given list was found, it is returned
    by the function.

    Parameters
    ----------
    labels : list[str | None]
        List of labels defined as `str` or undefined as `None`

    Returns
    -------
    str | None
        Unique label from the given list or undefined label as `None`
    """
    labels = set(labels)
    if len(labels) == 1:
        if label := labels.pop():
            return label
