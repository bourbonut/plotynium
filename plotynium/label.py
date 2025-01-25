def reduce(labels):
    labels = set(labels)
    if len(labels) == 1:
        if label := labels.pop():
            return label
