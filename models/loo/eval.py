
def accuracy(predictions, labels):
    """
    Calculates the accuracy of the predictions given the true labels.

    Parameters:
    predictions (list): A list of predicted labels.
    labels (list): A list of true labels.

    Returns:
    float: The accuracy of the predictions.
    """
    correct = 0
    total = len(predictions)
    for i in range(total):
        if predictions[i] == labels[i]:
            correct += 1
    return float(correct) / total


def f1(predictions, labels):
    """
    Calculates the F1 score of the predictions given the true labels.

    Parameters:
    predictions (list): A list of predicted labels.
    labels (list): A list of true labels.

    Returns:
    float: The F1 score of the predictions.
    """
    tp = 0
    fp = 0
    fn = 0
    for i in range(len(predictions)):
        if predictions[i] == labels[i]:
            if predictions[i] == 1:
                tp += 1
        else:
            if predictions[i] == 1:
                fp += 1
            else:
                fn += 1
    if tp == 0:
        return 0
    precision = float(tp) / (tp + fp)
    recall = float(tp) / (tp + fn)
    return 2 * precision * recall / (precision + recall)


def precision(predictions, labels):
    """
    Calculates the precision of the predictions given the true labels.

    Parameters:
    predictions (list): A list of predicted labels.
    labels (list): A list of true labels.

    Returns:
    float: The precision of the predictions.
    """
    tp = 0
    fp = 0
    for i in range(len(predictions)):
        if predictions[i] == labels[i]:
            if predictions[i] == 1:
                tp += 1
        else:
            if predictions[i] == 1:
                fp += 1
    if tp == 0:
        return 0
    return float(tp) / (tp + fp)

def recall(predictions, labels):
    """
    Calculates the recall of the predictions given the true labels.

    Parameters:
    predictions (list): A list of predicted labels.
    labels (list): A list of true labels.

    Returns:
    float: The recall of the predictions.
    """
    tp = 0
    fn = 0
    for i in range(len(predictions)):
        if predictions[i] == labels[i]:
            if predictions[i] == 1:
                tp += 1
        else:
            if predictions[i] == 0:
                fn += 1
    if tp == 0:
        return 0
    return float(tp) / (tp + fn)
