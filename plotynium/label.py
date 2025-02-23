def reduce(labels: list[str | None]) -> str:
    labels = set(labels)
    if len(labels) == 1:
        if label := labels.pop():
            return label
