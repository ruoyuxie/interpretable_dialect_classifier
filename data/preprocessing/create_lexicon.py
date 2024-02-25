import glob
import os
import re
import sys
import nltk
import Levenshtein

def get_silver_lexicon(lexicon):
    # get the silver lexicon
    silver_lexicon = {}
    for source_word in lexicon:
        
        # if there is only one target word, then it is the silver lexicon
        if len(lexicon[source_word]) == 1:
            silver_lexicon[source_word] = [lexicon[source_word][0][0]]
            continue
        
        # when the fequency is greater than 10, if the first target word has 2 times more the frequency of the second target word, then it is the silver lexicon
        if len(lexicon[source_word]) > 10 and lexicon[source_word][0][1] > 2 * lexicon[source_word][1][1]:
            silver_lexicon[source_word] = [lexicon[source_word][0][0]]
            continue

        # calculate the Levenshtein distance between the source word and the target words, the silver lexicon is the target word with the smallest Levenshtein distance
        target_words = [target_word[0] for target_word in lexicon[source_word]]
        distances = [Levenshtein.distance(source_word, target_word) for target_word in target_words]
        silver_lexicon[source_word] = [target_words[distances.index(min(distances))]]
        continue

    return silver_lexicon

# read alignment output file, text file
# return a list of tuples, each tuple contains the source phrase, target phrase, and alignment
def read_alignment_file(alignment_out_path, text_file_path):
    # read the alignment file
    with open(alignment_out_path, "r") as f1:
        alignment_text = f1.readlines()
    # read the source file
    with open(text_file_path, "r") as f2:
        text = f2.readlines()

    # create a list of tuples, each tuple contains the source phrase, target phrase, and alignment
    alignment_list = []
    for i in range(len(alignment_text)):
        # get the alignment
        alignment = alignment_text[i].strip()
        # get the source phrase
        source_phrase = text[i].strip()
        # add the tuple to the list
        alignment_list.append((text, alignment))

    return alignment_list

def main(language_folder):

    try:
        # os.mkdir(language_folder + "lexicon")
        # use path join to create the required files
        alignment_out = os.path.join(language_folder, "combined.out")
        text_file = os.path.join(language_folder, "combined")
        lexicon_file = os.path.join(language_folder, "lexicon")

    except:
        print(f"Error: {language_folder} does not contain the required files")
        return

    alignment_text = read_alignment_file(alignment_out,text_file)

    lexicon = {}

    for index, line in enumerate(alignment_text):
        text, alignment = line
        source_text , target_text = text[index].split(" ||| ") 
        target_text = target_text.strip().split()
        source_text = source_text.strip().split()
        for pair in alignment.split():
            source_index, target_index = pair.split("-")
            #print(source_text[int(source_index)], target_text[int(target_index)])
            if source_text[int(source_index)] not in lexicon:
                lexicon[source_text[int(source_index)]] = {}
            if target_text[int(target_index)] not in lexicon[source_text[int(source_index)]]:
                lexicon[source_text[int(source_index)]][target_text[int(target_index)]] = 0
            lexicon[source_text[int(source_index)]][target_text[int(target_index)]] += 1

    # sort the lexicon by the frequency of the target word
    for source_word in lexicon:
        lexicon[source_word] = sorted(lexicon[source_word].items(), key=lambda x: x[1], reverse=True)

    # write the lexicon to a file
    with open(lexicon_file, "w") as f1:
        for source_word in lexicon:
            f1.write(source_word)
            f1.write(" - ")
            for target_word in lexicon[source_word]:
                f1.write(target_word[0])
                f1.write(":")
                f1.write(str(target_word[1]))
                f1.write("\t")
            f1.write("\n")

    # get the silver lexicon
    silver_lexicon = get_silver_lexicon(lexicon)

    # write the silver lexicon to a file
    with open(lexicon_file + "_silver", "w") as f2:
        for source_word in silver_lexicon:
            # make sure both side are different
            if source_word == silver_lexicon[source_word][0]:
                continue
            f2.write(source_word)
            f2.write(" - ")
            f2.write(silver_lexicon[source_word][0])
            f2.write("\n")

if __name__ == "__main__":

    language_folder = "/scratch/rxie/selfexplain/my-self-exp/data/it/xls/alignment_files/"
    # call main for every subfolder in the language folder
    for subfolder in os.listdir(language_folder):
        main(os.path.join(language_folder, subfolder))

