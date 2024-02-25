#-*- coding: utf-8 -*-
import ast
import json
import csv
import random
import sys
import pandas as pd
import os

TOP_EXPLANATIONS = 5


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
            if "loo" in csv_file_path:
                # ingore if the word is a float or int numbers
                try:
                    float(word)
                    continue
                except ValueError:
                    pass
            if word != "":
                word_list.append(word)
        interpretations.append(word_list[:5])

    labels = []
    for row in df['predicted_labels']:
        labels.append(row)

    if len(interpretations) != len(labels):
        print("Error: interpretations and labels have different lengths")
        exit()

    return interpretations, labels

def main ():

    input_folder = "data/loo/zh/exp"
    # read files from input folder
    input_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    for file in input_files:
        print("Processing file: " + file)
        lil, labels = read_lil_interpretations_from_csv(os.path.join(input_folder, file))
        # combine each entry in lil into sentences with its corresponding label
        sentences = []
        for sent, label in zip(lil, labels):
            sent = " ".join(sent)
            sentences.append((sent, label))

        out_name = ""
        # write to tsv file, store in previous folder
        if "test" in file:
            out_name = "test"
        elif "dev" in file:
            out_name = "dev"
        elif "train" in file:
            out_name = "train"

        output_file_path = os.path.join(input_folder, "..", out_name + ".tsv")

        with open(output_file_path, 'w', encoding="utf-8") as output_file:
            output_file.write("sentence\tlabel\n")
            for sent, label in sentences:
                output_file.write(sent + "\t" + str(label) + "\n")




if __name__ == '__main__':
    main()