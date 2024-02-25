# read csv file and return a list of words from class0_1.csv
import csv
import random


def read_words(filename):
    # read csv file
    with open(filename, newline='',encoding="utf8") as f:
        # class zero words are all in column 0, class one words are all in column 1
        reader = csv.reader(f)
        # read all words in column 0 and column 1
        words = list(reader)
        # words is a list of lists, so we need to flatten it
        words = [item for sublist in words for item in sublist]
        # return the list of words

        class_zero_words = []
        class_one_words = []

        for item in words:
            if item == '':
                continue

            if len(item.split("\t")) != 2:
                class_zero_words.append(item)
            else:
                if item.split("\t")[0] != '':
                    class_zero_words.append(item.split("\t")[0])
                if item.split("\t")[1] != '':
                    class_one_words.append(item.split("\t")[1])

        # deduplicate the list
        class_zero_words = list(dict.fromkeys(class_zero_words))
        class_one_words = list(dict.fromkeys(class_one_words))

        return class_zero_words, class_one_words

class_zero_words, class_one_words = read_words('class0_1.csv')
# print("[class_zero_words]")
# for i in class_zero_words:
#     print(i)
# print("*"*100+"\n")
# print("[class_one_words]")
# for i in class_one_words:
#     print(i)

# concatenate the two lists
all_words = class_zero_words + class_one_words
# shuffle the list
random.shuffle(all_words)
for i in all_words:
    print(i)
