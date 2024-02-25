# -*- coding: utf-8 -*-
import os
import glob
import random

from transformers import AutoTokenizer
import jieba
import nltk
import re

seed = 42
random.seed(seed)

def read_tsv_file(tsv_file):
    with open(tsv_file, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        target = []
        for line in lines:
            line = line.strip()
            _, sent = line.split('\t')
            target.append(sent)

    return target

def clean (sent):
    # remove the punctuations
    sent = re.sub(r'[^\w\s]', '', sent)
    # remove the numbers
    sent = re.sub(r'\d+', '', sent)
    # remove the extra spaces
    sent = re.sub(r'\s+', ' ', sent)
    # remove the leading and trailing spaces
    sent = sent.strip()
    return sent

# user transformers tokenizer to tokenize the sentences
def tokenize_and_clean (file_name, data):
    tokenized = []

    if "pt" in file_name:
        for sent in data:
            tokens = nltk.word_tokenize(sent, language='portuguese')
            tokens = " ".join(tokens)
            tokens = clean(tokens)
            tokenized.append(tokens)

    elif "zh" in file_name:
        if "TW" in file_name:
            jieba.set_dictionary('dict.txt.big')
        else:
            jieba.set_dictionary('dict.txt.small')
        for sent in data:
            seg_list = jieba.cut(sent)
            # if the word is not Chinese, then it is a space
            seg_list = [word if re.match(r'[\u4e00-\u9fff]+', word) else '' for word in seg_list]
            tokenized_sent = (" ".join(seg_list))
            tokenized_sent = clean(tokenized_sent)

            tokenized.append(tokenized_sent)

    return tokenized

def combine_left_right(left, right):
    combined = []
    # make sure the length of left and right are the same
    assert len(left) == len(right)
    for i in range(len(left)):
        combined.append(left[i] + " ||| " + right[i])
    return combined

# read each folder in the frmt_dataset folder
for bucket in glob.glob('frmt_dataset/*'):

    pt_br = []
    pt_pt = []
    zh_cn = []
    zh_tw = []

    # read combined folder in the bucket
    combined_folder = os.path.join(bucket, 'combined')
    if not os.path.exists(combined_folder):
        os.makedirs(combined_folder)
    for tsv_file in glob.glob(combined_folder + '/*.tsv'):
        # if the file starts with 'pt' then it is pt file
        file_name = os.path.basename(tsv_file)
        if file_name.startswith('pt'):
            if file_name.endswith('BR.tsv'):
                pt_br = read_tsv_file(tsv_file)
                # tokenize the sentences
                pt_br = tokenize_and_clean(file_name,pt_br)
            elif file_name.endswith('PT.tsv'):
                pt_pt = read_tsv_file(tsv_file)
                # tokenize the sentences
                pt_pt = tokenize_and_clean(file_name,pt_pt)
        elif file_name.startswith('zh'):
            if file_name.endswith('CN.tsv'):
                zh_cn = read_tsv_file(tsv_file)
                # tokenize the sentences
                zh_cn = tokenize_and_clean(file_name,zh_cn)
            elif file_name.endswith('TW.tsv'):
                zh_tw = read_tsv_file(tsv_file)
                # tokenize the sentences
                zh_tw = tokenize_and_clean(file_name,zh_tw)

    combined_pt = combine_left_right(pt_br, pt_pt)
    combined_zh = combine_left_right(zh_cn, zh_tw)

    # write the combined files to the parallel folder
    parallel_folder = os.path.join(combined_folder, 'parallel')
    if not os.path.exists(parallel_folder):
        os.makedirs(parallel_folder)
    with open(os.path.join(parallel_folder, 'pt.tsv'), 'w') as f:
        f.write('\n'.join(combined_pt))
    with open(os.path.join(parallel_folder, 'zh.tsv'), 'w') as f:
        f.write('\n'.join(combined_zh))

    # todo: create selfexp dataset
    # eg: CN 0
    #     TW 1
    # ---------------
    #     BR 0
    #     PT 1

    # write the combined files to the self_exp_data folder
    self_exp_folder = os.path.join(combined_folder, 'self_exp_data')
    if not os.path.exists(self_exp_folder):
        os.makedirs(self_exp_folder)
    with open(os.path.join(self_exp_folder, 'pt.tsv'), 'w') as f:
        # split the sentences into two parts with the delimiter ' ||| '
        for sent in combined_pt:
            left, right = sent.split(' ||| ')
            f.write(left + '\t' + '0' + '\n')
            f.write(right + '\t' + '1' + '\n')

    with open(os.path.join(self_exp_folder, 'zh.tsv'), 'w') as f:
        # split the sentences into two parts with the delimiter ' ||| '
        for sent in combined_zh:
            left, right = sent.split(' ||| ')
            f.write(left + '\t' + '0' + '\n')
            f.write(right + '\t' + '1' + '\n')

# combine all self_exp_data from each bucket to one file
all_pt = []
all_zh = []
for bucket in glob.glob('frmt_dataset/*'):
    combined_folder = os.path.join(bucket, 'combined')
    self_exp_folder = os.path.join(combined_folder, 'self_exp_data')
    for tsv_file in glob.glob(self_exp_folder + '/*.tsv'):
        file_name = os.path.basename(tsv_file)
        with open(tsv_file, 'r', ) as f1:
            tsv_file = f1.readlines()

            if file_name.startswith('pt'):
                if file_name.startswith('pt'):
                    all_pt += tsv_file
            elif file_name.startswith('zh'):
                    all_zh += tsv_file

with open('frmt-clean/all_pt.tsv', 'w') as f:
    random.shuffle(all_pt)
    for sent in all_pt:
        f.write(sent)

with open('frmt-clean/all_zh.tsv', 'w') as f1:
    random.shuffle(all_zh)
    for sent in all_zh:
        f1.write(sent)

#split the data into train, dev, test
for lang in ['pt', 'zh']:
    with open('frmt-clean/all_{}.tsv'.format(lang), 'r') as f:
        data = f.readlines()
        # shuffle the data
        random.shuffle(data)
        # split the data into train, dev, test
        train = data[:int(len(data) * 0.8)]
        dev = data[int(len(data) * 0.8):int(len(data) * 0.9)]
        test = data[int(len(data) * 0.9):]
        # write the data to the train, dev, test files to split folder
        with open('frmt-clean/split/{}/train.tsv'.format(lang), 'w') as f1:
            f1.write("sentence\tlabel\n")
            for sent in train:
                f1.write(sent)
        with open('frmt-clean/split/{}/dev.tsv'.format(lang), 'w') as f2:
            f2.write("sentence\tlabel\n")
            for sent in dev:
                f2.write(sent)
        with open('frmt-clean/split/{}/test.tsv'.format(lang), 'w') as f3:
            f3.write("sentence\tlabel\n")
            for sent in test:
                f3.write(sent)
