import json


def main (path, gt):

    gt_class_0 = gt[0]
    gt_class_1 = gt[1]
    words_class_0 = []
    words_class_1 = []

    with open(path, 'r', encoding = "utf-8") as input_file:
        for k, line in enumerate(input_file):
            json_line = json.loads(line)
            sentence = json_line["sentence"]
            label = json_line["label"]
            words = sentence.split()

            if label == "0":
                for gt_word in gt_class_0:
                    if gt_word in words:
                        for w in words:
                            if w != gt_word:
                                words_class_0.append(w)

            elif label == "1":
                for gt_word in gt_class_1:
                    if gt_word in words:
                        for w in words:
                            if w != gt_word:
                                words_class_1.append(w)


    print("Class 0: ", gt_class_0)
    print("Class 1: ", gt_class_1)
    print("number of Class 0 words: ", len(words_class_0))
    print("number of Class 1 words: ", len(words_class_1))

    # get the most frequent words in class 0
    print("Most frequent words in class 0: ", get_most_frequent_words(words_class_0))
    # get the most frequent words in class 1
    print("Most frequent words in class 1: ", get_most_frequent_words(words_class_1))

def get_most_frequent_words(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_count[:10]

if __name__ == '__main__':

    gt_ofl_vs_non_ofl = [["mik","dik"],["mi","di"]]
    gt_de_vs_nl = [["hoes","veur"],["Huus","för"]]
    gt = []

    #json_file_path = "/scratch/rxie/selfexplain/my-self-exp/data/de/use_all_train/de_nl/test_with_parse.json"
    json_file_path = "/scratch/rxie/selfexplain/my-self-exp/data/de/de_nl/test_with_parse.json"
    ofl_flag = False
    de_nl_flag = True

    if ofl_flag is True:
        gt = gt_ofl_vs_non_ofl
    elif de_nl_flag is True:
        gt = gt_de_vs_nl

    main(json_file_path, gt)