import argparse
import Levenshtein

def exact_match(prediction, label, case_sensitive=True):
    if case_sensitive:
        return int(prediction.strip() == label.strip())
    else:
        return int(prediction.strip().lower() == label.strip().lower())

def cer(prediction, label, case_sensitive = True):
    prediction = prediction if case_sensitive else prediction.lower()
    label = label if case_sensitive else label.lower()

    edit_ops = Levenshtein.editops(prediction, label)
    edit_dist = len(edit_ops)
    num_insert = len([ops for ops in edit_ops if ops[0] == 'insert'])

    return edit_dist / (len(prediction) + num_insert)

def wer(prediction, label, case_sensitive=True):
    prediction = prediction if case_sensitive else prediction.lower()
    label = label if case_sensitive else label.lower()

    pred_tokens = prediction.strip().split()
    label_tokens = label.strip().split()

    # build vocab list
    vocab = set(pred_tokens + label_tokens)
    vocab_idx = {word: idx for idx, word in enumerate(vocab)}

    # convert tokens into indices
    pred_indices = [vocab_idx[token] for token in pred_tokens]
    label_indices = [vocab_idx[token] for token in label_tokens]

    # convert each number into char -> concat into string
    pred_str = "".join([chr(index) for index in pred_indices])
    label_str = "".join([chr(index) for index in label_indices])

    # get error rate 
    return cer(pred_str, label_str, case_sensitive)

def score(predictions, labels, case_sensitive):

    assert len(predictions) == len(labels)

    em_scores = []
    cer_scores = []
    wer_scores = []

    for prediction, label in zip(predictions, labels):
        em_scores.append(exact_match(prediction, label, case_sensitive))
        cer_scores.append(cer(prediction, label, case_sensitive))
        wer_scores.append(wer(prediction, label, case_sensitive))

    return {
        'exact_match': sum(em_scores) / len(em_scores),
        'cer': sum(cer_scores) / len(cer_scores),
        'wer': sum(wer_scores) / len(wer_scores)
    }


def read_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def read_tab_separated_file(filename):
    predictions = []
    labels = []
    with open(filename, 'r') as f:
        for line in f:
            pred, label = line.split('\t')
            predictions.append(pred.strip())
            labels.append(label.strip())
    return predictions, labels

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments to evaluate OCR')
    parser.add_argument('--predictions', type=str, help='File that consists of a list of predictions')
    parser.add_argument('--labels', type=str, help='File that consists of a list of labels')
    parser.add_argument('--pred-label-pair', type=str, help='File that consists of a list of prediction, label pair')

    args = parser.parse_args()

    if (args.pred_label_pair is None) and (args.predictions is None and args.labels is None):
        raise AssertionError("You need to provide a file for evaluation. Use --help for getting more info.")


    predictions = []
    labels = []

    # Input By Two Files
    if args.pred_label_pair is None:
        if args.predictions is None or args.labels is None:
            raise AssertionError("You need to provide both files for predictions and labels")
    
        predictions = read_file(args.predictions)
        labels = read_file(args.labels)

    # Input by a single file, each line consists of prediction and label separated by tab
    else:
        predictions, labels = read_tab_separated_file(args.pred_label_pair)

    # Valdiation
    assert len(predictions) > 0
    assert len(labels) > 0
    assert len(predictions) == len(labels)
    
    print(score(predictions, labels, case_sensitive=False))


