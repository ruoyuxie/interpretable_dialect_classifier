import os
import sys  
import json
import numpy as np

# read a tsv file and separate it into two columns, sentence and label
def read_tsv_files(file_path):
    file = []
    # read the tsv file and store it into a list
    with open(file_path, 'r',encoding="utf-8") as f:
        # read the file line by line, the first line should start with "句子	算法 X	算法 Y..."
        
        next(f)
        for line in f:
            if len(line.strip().split('\t'))!=2:
                continue
            try:
                sent, label = line.strip().split('\t')
            except:
                print(line)
                exit(1)
            # only keep the first k characters of the sentence split by space
            sent = " ".join(sent.split(" "))
            if sent == "" or sent == " ":
                continue
            file.append([sent, label])

    return file

def main (folder_path):
    # do this for test.tsv, train.tsv and dev.tsv in the directory
    for file_name in os.listdir(folder_path):

        if file_name.endswith('.tsv'):
            
            file_path = os.path.join(folder_path, file_name)

            # read the tsv file and process it
            file = read_tsv_files(file_path)

            # count the length of each sentence
            sent_length = []
            for line in file:
                sent_length.append(len(line[0].split(" ")))

            # print the average length of the sentences
            print(f"Average length of sentences in {file_name}: {np.mean(sent_length)}")

folder_path = "/scratch/rxie/selfexplain/my-self-exp/data/frmt-clean/split/zh"

main(folder_path=folder_path)
