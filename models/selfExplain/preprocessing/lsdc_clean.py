# -*- coding: utf-8 -*-
import logging
import os
import re
import glob
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sacremoses import MosesTruecaser
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

MAX_SENT_LENGTH = 250
seed = 42
random.seed(seed)
DE_LABELS = {'OWL': 0, 'OFL': 1, 'HAM': 2, 'HOL': 3, 'SUD': 4, 'MKB': 5, 'DRE': 6, 'ACH': 7, 'NPR': 8, 'NNI': 9,
             'OVY': 10, 'OFR': 11, 'MAR': 12, 'TWE': 13, 'MON': 14, 'GRO': 15}


def split_train_dev(infile, split_size):
    with open(infile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()
        reader = reader[1:]  # skip header
        print("Data size: ", len(reader))

        # split data into train.tsv and test.tsv and dev.tsv
        train, dev = train_test_split(reader, test_size=split_size, random_state=42)
        # split dev into dev.tsv and test.tsv
        dev, test = train_test_split(dev, test_size=0.5, random_state=42)

        print("Train size: ", len(train))
        print("Dev size: ", len(dev))
        print("Test size: ", len(test))
        print("-" * 50)

        data_path = os.path.dirname(infile)

        with open(data_path + "/train.tsv", "w", encoding="utf8") as open_file1:
            open_file1.write(("sentence" + "\t" + "label" + "\n"))
            open_file1.writelines(train)

        with open(data_path + "/dev.tsv", "w", encoding="utf8") as open_file2:
            open_file2.write(("sentence" + "\t" + "label" + "\n"))
            open_file2.writelines(dev)

        with open(data_path + "/test.tsv", "w", encoding="utf8") as open_file3:
            open_file3.write(("sentence" + "\t" + "label" + "\n"))
            open_file3.writelines(test)

        open_file.close()



def get_data_statistics_de_all(inputfile):
    print("*" * 50)
    print("Getting data statistics for: ", inputfile)
    with open(inputfile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()
        # create a list with 16 zeros
        label_count = [0] * 16
        for line in reader:
            if line != "\n" and line != "":
                try:
                    label, _, sentence = line.split("\t")
                except:
                    logging.info("skipping invalid sentence:", line)
                    continue

                # check if a sentence is in the reader more than once
                if reader.count(line) > 1:
                    logging.info("sentence is in reader more than once: ", line)

                if label not in DE_LABELS:
                    logging.error("Label not found: %s", label)

                label = int(DE_LABELS[label])

                if re.search('[a-zA-Z]', sentence) is not None:
                    label_count[label] = label_count[label] + 1

        plt.bar(DE_LABELS.keys(), label_count)
        plt.show()
        print("*********************************")
        print("number of total sentences: ", len(reader))
        for key, value in DE_LABELS.items():
            print(key, ":", label_count[value])
        print("*********************************")


def tokenzier_truecaser(inputfile, outputfile):
    with open(inputfile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()
    output_file = open(outputfile, "wb")
    mtr = MosesTruecaser()

    tok_sentances = []
    tok_sentances_with_label = []
    dup_sentances = []

    for line in reader:
        if line != "\n" and line != "" :
            try:
                label, _, sentence = line.split("\t")
            except:
                print("skipping invalid sentence:", line)
                continue

            if label not in DE_LABELS:
                logging.error("Label not found: %s", label)
            label = DE_LABELS[label]

            if re.search('[a-zA-Z]', sentence) is not None:

                tok_sentance = word_tokenize(sentence)

                if tok_sentance not in tok_sentances:
                    tok_sentances.append(tok_sentance)
                    tok_sentances_with_label.append(" ".join(tok_sentance) + "\t"+ str(label))
                else:
                    dup_sentances.append(" ".join(tok_sentance) + "\t"+ str(label))

    print("number of unique labels: ", len(DE_LABELS))
    print("labels: ", DE_LABELS)
    print("number of unique sentences: ", len(tok_sentances))
    print("number of duplicate sentences: ", len(dup_sentances))


    if os.path.exists(outputfile + ".truecasemodel") is not True:
        mtr.train(tok_sentances, save_to=outputfile + ".truecasemodel")

    my_truecaser = MosesTruecaser(outputfile + ".truecasemodel")

    output_file.write(("sentence" + "\t" + "label" + "\n").encode("utf8"))
    truecased_sentances = []
    for sentance_with_label in tok_sentances_with_label:
        sentence, label  = sentance_with_label.split("\t")
        truecased_sentance = " ".join(my_truecaser.truecase(sentence))+ "\t"+ str(label)

        if truecased_sentance not in truecased_sentances and truecased_sentances.count(truecased_sentance) < 2:
            truecased_sentances.append(truecased_sentance)
        # else:
        #     print("duplicate truecased sentence: ", truecased_sentance)

    final_truecased_sentances = list(de_duplicate(truecased_sentances))
    output_file.write(("\n".join(final_truecased_sentances)).encode("utf8"))
    output_file.close()

def de_duplicate(input_sents):
    seen = set()
    for sent in input_sents:
        if sent not in seen:
            yield sent
            seen.add(sent)


def four_way_classification(inputfile, outputfile):
    with open(inputfile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()

    with open(outputfile, "w", encoding="utf8") as open_file:
        reader = reader[1:]  # skip header
        open_file.write("sentence" + "\t" + "label" + "\n")

        for line in reader:
            if line != "\n" and line != "":
                sentence, label = line.split("\t")
                label = label.replace("\n", "")
                # 'OWL': 0, 'HOL': 3, 'SUD': 4, 'MKB': 5
                if label == '5':
                    open_file.write(sentence + "\t" + "0" + "\n")
                elif label == '4':
                    open_file.write(sentence + "\t" + "1" + "\n")
                elif label == '0':
                    open_file.write(sentence + "\t" + "2" + "\n")
                elif label == '3':
                    open_file.write(sentence + "\t" + "3" + "\n")


def binary_classification(inputfile, outputfile):
    with open(inputfile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()

    with open(outputfile, "w", encoding="utf8") as open_file:
        reader = reader[1:]  # skip header
        open_file.write("sentence" + "\t" + "label" + "\n")

        for line in reader:
            if line != "\n" and line != "":
                sentence, label = line.split("\t")
                label = label.replace("\n", "")
                # 'OWL': 0, 'HOL': 3, 'SUD': 4, 'MKB': 5
                # MKB, MAR, NPR, East Frisian (OFR), and Gronings (GRO)
            #     DE_LABELS = {'OWL': 0, 'OFL': 1, 'HAM': 2, 'HOL': 3, 'SUD': 4, 'MKB': 5, 'DRE': 6, 'ACH': 7, 'NPR': 8, 'NNI': 9,
            #  'OVY': 10, 'OFR': 11, 'MAR': 12, 'TWE': 13, 'MON': 14, 'GRO': 15}

# plural_suffix:                 if label == '6' or label == '12' or label == '8' or label == '11' or label == '15':
# de==1 vs nl ==0:                     if label == '6' or label == '7' or label == '15' or label == '10' or label == '13':

                if label == '6' or label == '7' or label == '15' or label == '10' or label == '13':   
                    open_file.write(sentence + "\t" + "0" + "\n")
                else:
                    open_file.write(sentence + "\t" + "1" + "\n")
        open_file.close()


def pairwise_binary_classification(inputfile):
    with open(inputfile, "r", encoding="utf8") as open_file:
        reader = open_file.readlines()

        # get path of current input folder
        path = os.path.dirname(inputfile)

        # create a folder for the output files
        pairwise_output_folder = path + "/pairwise"
        if not os.path.exists(pairwise_output_folder):
            os.makedirs(pairwise_output_folder)

        # select one label and create a file for each label
        for current_label in DE_LABELS:
            # create a folder for the current label
            current_label_folder = pairwise_output_folder + "/" + current_label
            if not os.path.exists(current_label_folder):
                os.makedirs(current_label_folder)

            current_file = current_label_folder + "/" + "all.tsv"
            with open(current_file, "w", encoding="utf8") as open_file1:
                open_file1.write("sentence" + "\t" + "label" + "\n")
                current_label_count = 0
                else_label_count = 0

                for line in reader:
                    if line == "sentence\tlabel\n":
                        continue

                    if line != "\n" and line != "":
                        try:
                            sentence, sent_label = line.split("\t")
                            sent_label = int(sent_label.replace("\n", ""))

                        except:
                            print("skipping invalid sentence:", line)
                            continue

                        # current language label is 1, all other labels are 0
                        if sent_label == DE_LABELS[current_label]:
                            open_file1.write(sentence + "\t" + "1" + "\n")
                            current_label_count += 1
                        # all other languages are labeled as 0
                        else:
                            open_file1.write(sentence + "\t" + "0" + "\n")
                            else_label_count += 1
                open_file1.close()

                print("file created: ", current_file)
                # print current label and its count
                print("current label: ", current_label, " count: ", current_label_count)
                # print all other labels and their count
                print("all other labels count: ", else_label_count)
                print("-" * 50)
            open_file.close()

    # delete the original file


def process_germen_data(raw_input_file):
    tokenzie_file = raw_input_file + ".tok"
    binary_flag = True
    four_way = False
    pairwise =  False

    if os.path.exists(tokenzie_file) is not True:
        tokenzier_truecaser(raw_input_file, tokenzie_file)
    print("Tokenize and truecase done!")

    if binary_flag is True:
        binary_classification(tokenzie_file, tokenzie_file + ".bin")
        print("Binary  data selection done!")
    elif four_way is True:
        four_way_classification(tokenzie_file, tokenzie_file + ".4way")
        print("Four way data selection done!")
    elif pairwise is True:
        pairwise_binary_classification(tokenzie_file)
        print("Pairwise data selection done!")

    print("*********************************")

    print("Splitting data...")
    if binary_flag is True:
        split_train_dev(tokenzie_file + ".bin", 0.2)
    elif four_way is True:
        split_train_dev(tokenzie_file + ".4way", 0.2)
    elif pairwise is True:
        # split pairwise data for each folder in the pairwise folder (each folder contains one language) and create a train and dev tsv file
        data_path = os.path.dirname(tokenzie_file)
        for current_label in DE_LABELS:
            current_label_folder = data_path + "/pairwise/" + current_label
            split_train_dev(current_label_folder + "/all.tsv", 0.2)
            os.remove(current_label_folder + "/all.tsv")
    else:
        split_train_dev(tokenzie_file, 0.2)
    print("Splitting done!")


def get_data_statistics_de(input_folder):
    # get all.tsv files in the folder
    for file in glob.glob(input_folder + "/*"):
        if file.endswith(".tsv") is True:
            with open(file, "r", encoding="utf8") as open_file:
                reader = open_file.readlines()
                number_of_sentences = 0
                number_of_words = 0
                number_of_characters = 0
                longest_sentence_length = 0
                list_words = []
                for index, line in enumerate(reader):
                    if index > 0:
                        number_of_sentences += 1
                        sentence = line.split("\t")[0]
                        number_of_words += len(sentence.split(" "))
                        number_of_characters += len(sentence)
                        list_words.append(len(sentence.split(" ")))
                        if len(sentence) > longest_sentence_length:
                            longest_sentence_length = len(sentence)
                plt.plot(list_words, linestyle='dotted')
                plt.show()
                print("*********************************")
                print("File name: ", file)
                print("number of sentences: ", number_of_sentences)
                print("number of words: ", number_of_words)
                print("number of characters: ", number_of_characters)
                print("average number of words per sentence: ", number_of_words / number_of_sentences)
                print("median number of words per sentence: ", np.median(list_words))
                print("average number of characters per sentence: ", number_of_characters / number_of_sentences)
                print("longest sentence length: ", longest_sentence_length)
                print("max length sentence: ", max(list_words))
                print("*********************************")


def main():
    process_germen_data(raw_input_file="/scratch/rxie/selfexplain/my-self-exp/data/de/all/all.tsv")
    # get_data_statistics_de_all(inputfile="../data/de/all.tsv")


if __name__ == "__main__":
    main()
