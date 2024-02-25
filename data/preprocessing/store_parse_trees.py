# -*- coding: utf-8 -*-

import os
import argparse
import csv
import json
import random
from typing import Dict
import re
from constituency_parse import ParseTree
import build_concept_store
#from compound_split import char_split
import nltk
import sys
# nltk.download('punkt')

class ParsedDataset(object):
    def __init__(self, tokenizer_name):
        self.parse_trees: Dict[str, str] = {}
        self.parser = ParseTree(tokenizer_name=tokenizer_name)
        self.TOKEN_LIMIT = 250

    def break_into_small_sentences(self, sentence, trimmed_sentences):
        symbols = ["."]
        symbol = random.choice(symbols)

        # keep breaking sentence into smaller sentences until the length of the sentence is less than the random length limit
        while len(sentence) > self.TOKEN_LIMIT:
            random_length_limit = random.randint(50, self.TOKEN_LIMIT)
            last_period_index = sentence.rfind(symbol, 0, random_length_limit)
            if last_period_index != -1:
                trimmed_sentences.append(sentence[0:last_period_index + 1])
                sentence = sentence[last_period_index + 1:]
            else:
                trimmed_sentences.append(sentence[0:random_length_limit])
                sentence = sentence[random_length_limit:]

        trimmed_sentences.append(sentence)

        return trimmed_sentences

    def de_chunker(self, input_sent):

        final_sents = []

        tokenized_sent = input_sent.split(" ")
        combined_text = tokenized_sent[:self.TOKEN_LIMIT]

        for words in combined_text:
            split_words = max(char_split.split_compound(words))[1:]
            if len(split_words) > 1 and split_words[0] != split_words[1]:
                for word in split_words:
                    final_sents.append(word.lower())
                # print(words,"==>",split_words)
            else:
                final_sents.append(words)

        return " ".join(final_sents)


    def read_and_store_from_tsv(self, input_file_name, output_file_name, N, sub_word, de_chunker):
        with open(output_file_name, 'w', encoding="utf-8") as output_file:
            with open(input_file_name, 'r', encoding="utf-8") as open_file:
                reader = csv.reader(open_file, delimiter='\t')
                next(reader, None)  # skip header
                for row in reader:
                    try:
                        text, label = row
                    except:
                        print("skipping invalid line:", row)
                        continue
                    text = re.sub(r'[^\w\s]', '', text)
                    text = re.sub(' +', ' ', text)
                    text = text.strip()
                    # tokenzie the sentence
                    text = nltk.word_tokenize(text)
                    text = " ".join(text)
                    # lower case the sentence for pt and it
                    # ***DONT DO LOWER CASE FOR DE***
                    text = text.lower()

                    trimmed_sentences = []
                    trimmed_sentences = self.break_into_small_sentences(text, trimmed_sentences)
                    for sentence in text:
                        if len(sentence.strip().split(" ")) > N:

                            if N != 0 and de_chunker == 'true':
                                sentence = self.de_chunker(sentence)
                                
                            sentence = sentence.strip()

                            parse_tree, nt_idx_matrix = self.parser.get_parse_tree_for_raw_sent(raw_sent=sentence, N=N, sub_word=sub_word, de_chunker=de_chunker)

                            datapoint_dict = {'sentence': sentence,
                                              'parse_tree': parse_tree,
                                              'label': label,
                                              'nt_idx_matrix': nt_idx_matrix}
                            json.dump(datapoint_dict, output_file, ensure_ascii=False)
                            output_file.write('\n')
        return

    def store_parse_trees(self, output_file):
        with open(output_file, 'w', encoding="utf-8") as open_file:
            json.dump(self.parse_trees, open_file)
        return

    def get_ngram_corpus(self, input_file_name):
        vocabulary = []

        with open(input_file_name, 'r', encoding="utf-8") as open_file:
            reader = csv.reader(open_file, delimiter='\t')
            next(reader, None)  # skip header

            # count unique word in the dataset and store them in a list called vocabulary
            for row in reader:
                text = row[0].strip('\t').split()
                # print(text)
                for word in text:
                    if word not in vocabulary:
                        vocabulary.append(word)
        return vocabulary


def main():
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--data_dir", type=str, required=False,
                        help="The input data dir. Should contain the .tsv files (or other data files) for the task.")
    parser.add_argument("--tokenizer_name", default='xlm-roberta-base', type=str, required=False,
                        help="Tokenizer name, xlnet-base-cased, xlm-roberta-base or roberta-base")

    parser.add_argument("--number_of_grams", default='1', type=str, required=False,
                        help="Feature extractor, use ngram (set number > 0) or parse-tree (set number = 0)")
    parser.add_argument("--sub_word", default='false', type=str, required=False,
                        help="Use sub-word for N gram or not")

    parser.add_argument("--de_chunker", default='true', type=str, required=False,
                        help="Use noun phrase chunker for De or not")


    args = parser.parse_args()
    parsed_data = ParsedDataset(tokenizer_name=args.tokenizer_name)
    grams = int(args.number_of_grams)
    sub_word = args.sub_word

    # check if the input data directory exists
    if not os.path.exists(args.data_dir):
        print("The input data directory {} does not exist.".format(args.data_dir))
        sys.exit(1)
    
    avaliable_files = []
    # check if the input data directory contains train.tsv, dev.tsv, test.tsv, and update the avaliable_files list
    for file_split in ['train', 'dev', 'test']:
        input_file_name = args.data_dir + "/" + file_split + '.tsv'
        if os.path.exists(input_file_name):
            avaliable_files.append(file_split)
    print("The input data directory contains: ", avaliable_files)

    # Read input files from folder
    for file_split in avaliable_files:
        input_file_name = args.data_dir + "/" + file_split + '.tsv'
        output_file_name = args.data_dir + "/" + file_split + '_with_parse.json'

        parsed_data.read_and_store_from_tsv(input_file_name=input_file_name, output_file_name=output_file_name,
                                                N=grams, sub_word=sub_word, de_chunker=args.de_chunker)


    print("Convert to JSON file successfully!\n")
    build_concept_store_input = args.data_dir + "/train_with_parse.json"
    build_concept_store.concept_store(build_concept_store_input, args.data_dir, args.tokenizer_name, 5)
    print("Build concept store successfully!\n")

if __name__ == "__main__":
    main()
