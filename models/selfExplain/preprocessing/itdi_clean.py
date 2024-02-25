# -*- coding: utf-8 -*-
import logging
import os
import re
import sys
from collections import Counter
import glob
import json
import random
import Levenshtein
import numpy as np
from sklearn.model_selection import train_test_split
from sacremoses import MosesTruecaser
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

MAX_SENT_LENGTH = 250
seed = 42
random.seed(seed)


# 0 means dialect
# 1 means italian


def split_train_dev(infile, split_size):
    with open(infile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()
    reader = reader[1:]  # skip header
    print("Data size: ", len(reader))

    # split data into train.tsv and test.tsv
    train, dev = train_test_split(reader, test_size=split_size, random_state=42)

    print("Train size: ", len(train))
    print("Dev size: ", len(dev))

    with open(infile + ".train.tsv.split", "w", encoding="utf8") as open_file1:
        open_file1.write(("sentence" + "\t" + "label" + "\n"))
        open_file1.writelines(train)

    with open(infile + ".dev.tsv.split", "w", encoding="utf8") as open_file2:
        open_file2.write(("sentence" + "\t" + "label" + "\n"))
        open_file2.writelines(dev)


def tokenzier_truecaser(inputfile, outputfile):

    de_lables = {'OWL': 0, 'OFL': 1, 'HAM': 2, 'HOL': 3, 'SUD': 4, 'MKB': 5, 'DRE': 6, 'ACH': 7, 'NPR': 8, 'NNI': 9, 'OVY': 10, 'OFR': 11, 'MAR': 12, 'TWE': 13, 'MON': 14, 'GRO': 15}

    with open(inputfile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()
    output_file = open(outputfile, "wb")
    mtr = MosesTruecaser()

    tok_sentances = []
    tok_sentances_with_label = []

    for line in reader:
        if line != "\n" and line.__contains__("\t"):
            label, _, sentence = line.split("\t")

            if label not in de_lables:
                logging.error("Label not found: %s", label)
            label = de_lables[label]

            if re.search('[a-zA-Z]', sentence) is not None:
                tok_sentance = word_tokenize(sentence)
                tok_sentances.append(tok_sentance)
                tok_sentances_with_label.append(str(label) + "\t" + " ".join(tok_sentance))


    print("number of unique labels: ", len(de_lables))
    print("labels: ", de_lables)

    if os.path.exists(outputfile + ".truecasemodel") is not True:
        mtr.train(tok_sentances, save_to=outputfile + ".truecasemodel")

    my_truecaser = MosesTruecaser(outputfile + ".truecasemodel")

    output_file.write(("sentence" + "\t" + "label" + "\n").encode("utf8"))

    for line in tok_sentances_with_label:
        label, sentence = line.split("\t")
        output_file.write((my_truecaser.truecase(sentence, return_str=True) + "\t" + str(label) + "\n").encode("utf8"))


def binary_classification(inputfile, outputfile):
    with open(inputfile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()

    with open(outputfile, "w", encoding="utf8") as open_file:
        reader = reader[1:]  # skip header
        open_file.write("sentence" + "\t" + "label" + "\n")

        for line in reader:
            if line != "\n" and line.__contains__("\t"):
                sentence, label = line.split("\t")
                label = label.replace("\n", "")
                if label == '5':
                    open_file.write(sentence + "\t" + "0" + "\n")
                elif label == '4':
                    open_file.write(sentence + "\t" + "1" + "\n")


def get_label(inputfile):
    path = inputfile.split("/")  # split path
    label = ""
    for folder in path:
        if folder.__contains__("_texts"):
            label = folder.split("_")[0].upper()
            break
    return label


def too_much_numbers(sentence):
    # check if half of the sentence is numbers
    # if more than one third of the sentence is numbers, then it is not a valid sentence
    numbers = re.findall(r'\d+', sentence)
    if len(numbers) > len(sentence.split(' ')) / 3:
        return True
    else:
        return False


def sentence_validation_check(sentence):
    if sentence != "\n" and \
            sentence != "" and \
            sentence != " " and \
            len(sentence) > 5 \
            and sentence.count(";/") < 1 \
            and sentence.count("&lt;") < 1 \
            and sentence.count("&gt;") < 1 \
            and sentence.count("timestamp") < 1 \
            and sentence.count("username") < 1 \
            and sentence.count("wiki") < 1 \
            and sentence.count("__NOEDITSECTION__") < 1 \
            and sentence.__contains__("http://") is False \
            and too_much_numbers(sentence) is False \
            and re.search('[a-zA-Z]', sentence) is not None:

        return True

    else:
        return False


def sentences_are_similar(current_sentence, last_sentence):
    distance = Levenshtein.distance(current_sentence, last_sentence)
    if distance >= 30:
        return False
    else:
        return True


def break_into_small_sentences(sentence, trimmed_sentences):

    # use nltk sent tokenizer!!
    #
    symbols = ["."]
    symbol = random.choice(symbols)

    # keep breaking sentence into smaller sentences until the length of the sentence is less than the random length limit
    while len(sentence) > MAX_SENT_LENGTH:
        random_length_limit = random.randint(50, MAX_SENT_LENGTH)
        last_period_index = sentence.rfind(symbol, 0, random_length_limit)
        if last_period_index != -1:
            trimmed_sentences.append(sentence[0:last_period_index + 1])
            sentence = sentence[last_period_index + 1:]
        else:
            trimmed_sentences.append(sentence[0:random_length_limit])
            sentence = sentence[random_length_limit:]

    trimmed_sentences.append(sentence)

    return trimmed_sentences


def get_clean_sentence(text):
    sentence = text.strip(" ").strip("\n").replace("\n", "")
    sentence = sentence.replace("&lt;br&gt;", "")
    sentence = sentence.replace("&lt;br /&gt;", "")
    sentence = sentence.replace("&lt;br/&gt;", "")
    sentence = sentence.replace("&lt;br / &gt;", "")
    sentence = sentence.replace(";/", "")
    sentence = sentence.replace("&lt;", "")
    sentence = sentence.replace("&gt;", "")
    sentence = sentence.replace("\u00a0", " ")
    return sentence


def extract_sentences(inputfile, outputfile, label):
    with open(inputfile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()

    with open(outputfile, "w", encoding="utf8") as open_file:
        open_file.write("sentence" + "\t" + "label" + "\n")
        longest_sentence_length = 0
        number_of_extracted_sentences = 0
        output_sentences_list = []
        for index, line in enumerate(reader):
            last_text = json.loads(reader[index - 1])["text"]
            last_last_text = json.loads(reader[index - 2])["text"]
            current_text = json.loads(line)["text"]

            if sentences_are_similar(last_text, current_text) is False and sentences_are_similar(last_last_text,
                                                                                                 current_text) is False:
                sentence = get_clean_sentence(current_text)
                if sentence_validation_check(sentence):
                    trimmed_sentences = []
                    if len(sentence) > MAX_SENT_LENGTH:
                        for sub_sentence in break_into_small_sentences(sentence, trimmed_sentences):
                            if sentence_validation_check(sub_sentence):
                                if len(sub_sentence) > longest_sentence_length:
                                    longest_sentence_length = len(sub_sentence)
                                # remove sentence's starting spaces
                                sub_sentence = sub_sentence.strip(" ").strip("\n")
                                output_sentences_list.append(sub_sentence)
                                number_of_extracted_sentences += 1
                    else:

                        # remove sentence's starting spaces
                        sentence = sentence.strip(" ").strip("\n")
                        output_sentences_list.append(sentence)
                        number_of_extracted_sentences += 1
                    # if number_of_extracted_sentences == 14:
                    #     print("here")

        output_sentences_list = double_check_for_duplicates(output_sentences_list)

        for sentence in output_sentences_list:
            open_file.write(sentence + "\t" + label + "\n")


def double_check_for_duplicates(output_sentences_list):
    for index, sentence in enumerate(output_sentences_list):
        # compare current sentence with all.tsv the sentences after it to check if they are similar
        for next_sentence in output_sentences_list[index + 1:]:
            distance = Levenshtein.distance(sentence, next_sentence)
            if distance < 30:
                # print("duplicate found: \n", sentence, "\n",next_sentence)
                output_sentences_list.remove(next_sentence)
    return output_sentences_list


def get_data_statistics_it(data_path):
    with open(data_path, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()

        number_of_sentences = 0
        number_of_words = 0
        number_of_characters = 0
        list_words_len = []
        for index, line in enumerate(reader):
            if index > 0:
                number_of_sentences += 1
               # sentence = json.loads(line)["text"]
                sentence = line.split("\t")[0]
                number_of_words += len(sentence.split(" "))
                number_of_characters += len(sentence)
                list_words_len.append(len(sentence.split(" ")))
                # if len(sentence) > longest_sentence_length:
                #     longest_sentence_length = len(sentence)

        plt.plot(list_words_len, linestyle='dotted')
        plt.show()

        print("*********************************")
        print("file name: ", data_path)
        print("number of sentences: ", number_of_sentences)
        print("number of words: ", number_of_words)
        print("number of characters: ", number_of_characters)
        print(" average number of words per sentence: ", number_of_words / number_of_sentences)
        print("Median number of words per sentence: ", np.median(list_words_len))
        print("max length sentence: ", max(list_words_len))
        print("*********************************")

    # write the data statistics to a file
    # with open(data_path + "_data_statistics.txt", "w", encoding="utf8") as open_file:
    #     open_file.write("number of sentences: " + str(number_of_sentences) + "\n")
    #     open_file.write("number of words: " + str(number_of_words) + "\n")
    #     open_file.write("number of characters: " + str(number_of_characters) + "\n")
    #     open_file.write("average number of words per sentence: " + str(number_of_words / number_of_sentences) + "\n")
    #     open_file.write("average number of characters per sentence: " + str(number_of_characters / number_of_sentences) + "\n")
    #     open_file.write("longest sentence length: " + str(longest_sentence_length) + "\n")


def combine_extract_files(folder_path):
    with open(folder_path + "extracted.combined", "w", encoding="utf8") as open_file:
        open_file.write("sentence" + "\t" + "label" + "\n")
        for file in os.listdir(folder_path):
            if file.endswith(".extract"):
                with open(folder_path + file, "r", encoding="utf8") as open_file2:
                    reader = open_file2.readlines()
                    for index, line in enumerate(reader):
                        if index > 0:
                            open_file.write(line)


def process_italian_data(raw_italian_folder):
    # for sub_folder in glob.glob(raw_italian_folder + "/*"):
    #     sub_folder = sub_folder.replace("\\", "/")
    #     for AA in glob.glob(sub_folder + "/*"):
    #         label = get_label(AA)
    #
    #         for file in glob.glob(AA + "/*"):
    #             if file.endswith(".extract") is not True and file.__contains__("combined") is False\
    #                     and file.__contains__("statistics") is False:
    #                 extract_sentences(file, file + ".extract", label)
    #                 print("Extracting sentences from " + file + " done!\n")
    #
    #         combine_extract_files(AA + "/")
    #         get_data_statistics_it(AA + "/extracted.combined")
    #         print("Combining extracted sentences from " + label + " done!")
    #         print("************************************************************\n")
    #
    # # combine all.tsv the extracted.combined files from all.tsv the sub folders into one file
    # with open(raw_italian_folder + "all_extracted.combined", "w", encoding="utf8") as open_file:
    #     open_file.write("sentence" + "\t" + "label" + "\n")
    #     for sub_folder in glob.glob(raw_italian_folder + "/*"):
    #         sub_folder = sub_folder.replace("\\", "/")
    #         for AA in glob.glob(sub_folder + "/*"):
    #             with open(AA + "/extracted.combined", "r", encoding="utf8") as open_file2:
    #                 reader = open_file2.readlines()
    #                 for index, line in enumerate(reader):
    #                     if index > 0:
    #                         open_file.write(line)
    #
    # get_data_statistics_it(raw_italian_folder + "all_extracted.combined")
    # print("Combining extracted sentences from all.tsv the sub folders done!")
    # print("************************************************************\n")
    #

    extract_sentences(raw_italian_folder + "AA/wiki_00", raw_italian_folder + "AA/wiki_00.extract", "test.tsv-label")


def main():

    process_italian_data(raw_italian_folder="../temp")
    # process_italian_data(raw_italian_folder="../temp/eml_texts/")

    #get_data_statistics_it("..\data\wiki_italian_data\eml_texts\AA\wiki_01.extract")

    # get_data_statistics_it("..\data\De\multiclass/train.tsv.tsv")
    # get_data_statistics_it("..\data\De\multiclass/test.tsv.tsv")
    # get_data_statistics_it("..\data\De\multiclass/dev.tsv.tsv")


if __name__ == "__main__":
    main()