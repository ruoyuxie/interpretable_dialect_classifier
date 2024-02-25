#-*- coding: utf-8 -*-
import ast
import json
import csv
import random

import pandas as pd
TOP_EXPLANATIONS = 5

def read_sentence_from_json(json_file_path):
    with open(json_file_path, 'r', encoding="utf-8") as input_file:
        data = []
        for k, line in enumerate(input_file):
            json_line = json.loads(line)
            sentence = json_line["sentence"]
            data.append(sentence)
        # only keep first 50 sentences
        # data = data[:10]
    return data

def create_words_list(lang):
    lil_list = lang['lil_interpretations'].apply(lambda x: eval(x)).apply(lambda x: x[:TOP_EXPLANATIONS]).tolist()
    # for each element in lil_list, get the key of each tuple and add to a list
    words = []
    for i in range(len(lil_list)):
        # make sure all words share different probability
        if len(set([x[1] for x in lil_list[i]])) == 1:
            continue
        for j in range(len(lil_list[i])):
            if lil_list[i][j][0] != "" and len(lil_list[i][j][0]) > 1:
                words.append(lil_list[i][j])

    return words
def read_lil_interpretations_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path, header=0, sep='\t')

    interpretations = []
    # each doc is a list of words from lil_interpretations, which is a list of words from each row without scores
    for row in df['lil_interpretations']:
        row = row.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
        words = row.split(',')

        # Extract the words and add them to a list
        word_list = []
        for word in words:
            word = word.replace('(', '').replace(')', '').split('-')[0]
            if word != "":
                word_list.append(word)
        interpretations.append(word_list[:3])

    labels = []
    for row in df['predicted_labels']:
        labels.append(row)

    if len(interpretations) != len(labels):
        print("Error: interpretations and labels have different lengths")
        exit()

    return interpretations, labels

def combine_sentence_with_lil_interpretations(sentence, lil_interpretations, labels):
    combined = []
    if len(sentence) != len(lil_interpretations) != len(labels):
        print("Error: sentence and lil_interpretations have different lengths")
        exit()
    for i in range(len(sentence)):
        combined.append([labels[i], sentence[i], lil_interpretations[i]] )
    return combined

def main ():
    class_0_results = {}
    class_1_results = {}

    json_file_path="test_with_parse.json"
    csv_file_path="result_1gram.csv"

    sentence = read_sentence_from_json(json_file_path)
    lil_interpretations, labels = read_lil_interpretations_from_csv(csv_file_path)

    combined = combine_sentence_with_lil_interpretations(sentence, lil_interpretations, labels)

    sample_instances_class_0 = []
    # open the text file and read the sample sentences from loo experiment
    with open("loo_sample_instances_class_0.txt", 'r', encoding="utf-8") as input_file0:
        for line in input_file0:

            # if error: copy whole thing from excel sheet where \t is the default delimiter
            loo_sent = line.split("\t")[3].strip()

            # find the sample instances in the combined list, where the sentence is the same as the loo_sent
            for row in combined:
                if row[1] == loo_sent:
                    sample_instances_class_0.append(row)
                    break

    sample_instances_class_1 = []
    with open("loo_sample_instances_class_1.txt", 'r', encoding="utf-8") as input_file1:
        for line in input_file1:
            loo_sent = line.split("\t")[3].strip()

            # find the sample instances in the combined list, where the sentence is the same as the loo_sent
            for row in combined:
                if row[1] == loo_sent:
                    sample_instances_class_1.append(row)
                    break




    print("\nclass_0_sample:")
    for _, sentence, top_words in sample_instances_class_0:
        print(", ".join(top_words), ", ", sentence)

    print("\nclass_1_sample:")
    for _, sentence, top_words in sample_instances_class_1:
        print(", ".join(top_words), ", ", sentence)



if __name__ == '__main__':
    main()