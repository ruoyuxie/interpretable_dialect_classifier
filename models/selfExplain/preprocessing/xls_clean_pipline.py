# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import pandas as pd
import tqdm
import nltk
#import create_lexicon
import shutil
import random


# 0 means dialect
# 1 means italian


def clean_xls(path, target_region):
    file_name = os.path.basename(path)

    # open a xls file
    xls = pd.ExcelFile(path)
    # get the "Comune,Provincia,Regione" and "Frase" columns from the xls file
    df = xls.parse(xls.sheet_names[0], usecols=[1, 2, 4])
    # print(len(df))

    # rename the columns to "phrase" and "region" for convenience
    df = df.rename(columns={"Posizione": "phrase_index", "Comune,Provincia,Regione": "region", "Frase": "phrase"})

    #df = df.head(5)
    
    if len(df) < 10:
        print("WARNING: the length of dataframe is ", len(df))  

    standard_it = {}
    last_standard_it = []

    # for each row, if its region is not in target_region, print the row and drop it
    for index, row in df.iterrows():

        # skip the row if the row is empty
        if pd.isnull(row["phrase"]) or row["phrase"] == "omessa" or row["phrase"] == "-":
            continue

        # if the row's phase_index is not NaN, the row is a standard italian phrase, until the next row with phase_index is not NaN,
        # all the rows in between are the translations of the standard italian phrase
        if not pd.isnull(row["phrase_index"]):

            # make it a key in standard_it
            if row["phrase"] not in standard_it:
                standard_it[row["phrase"]] = []
                last_standard_it = list(standard_it.keys())[-1]

            else:
                last_standard_it = row["phrase"]

        # if the row's phase_index is NaN, the row is a translation of the standard italian phrase
        else:

            regions = row["region"].split(",")
            phase = row["phrase"]

            # if the row contains duplicated regions, delete the duplicated regions and keep the first one
            if len(regions) != len(set(regions)):
                regions = list(set(regions))
                # print("duplicated region", region, "in row", row)

            # if none of the regions in the row is in target_region, drop the row
            if not any(region in target_region for region in regions):
                df = df.drop(index)
                # print("dropped since no target regions there", row)
                continue

            # if abs(len(standard_it[0].split(" ")) - len(phase.split(" "))) > 0:
            #     df = df.drop(index)
            #     #print("dropped since phase length not equal", row)
            #     continue

            # if the row contains target regions, keep the row
            # else:
            #     #print("target region found", row)
            #     pass

            # if none of the regions in the row is in target_region, drop the row
            if not any(region in target_region for region in regions):
                df = df.drop(index)
                # print("dropped since no target regions there", row)
                continue

            # only keep the target regions in the row
            regions = [region for region in regions if region in target_region][0]

            # make sure the phrase is unique
            if len(df[df["phrase"] == phase]) > 1:
                df = df.drop(index)
                # print("dropped since phase not unique", row)
                continue

            phase = clean_sent(phase)

            phrase_region_tuple = (phase, regions)

            # add the translation to the last entry in standard_it, add the phrase_region_tuple to the last entry in standard_it
            # one standard italian phrase can have multiple translations
            if phrase_region_tuple not in standard_it[last_standard_it]:
                standard_it[last_standard_it].append(phrase_region_tuple)


    # clean_sent the keys in standard_it
    standard_it = {clean_sent(key): value for key, value in standard_it.items()}

    return standard_it


def clean_sent(sent):
    if "/" in sent:
        sent = sent.split("/")[0]

    sent = sent.strip()

    # remove the punctuations
    sent = re.sub(r'[^\w\s]+', '', sent)
    # tokenize the phrase
    sent = nltk.word_tokenize(sent)
    sent = " ".join(sent)

    return sent

def check_words(idti_line):
    for word in idti_line.split("\t")[0].split(" "):
        if len(word) > 20:
            return False
        # if the word contains islamic characters, skip the line
        if re.search(r"[\u0600-\u06FF]+", word) or re.search(r"[\u0590-\u05FF]",
                                                             word) or re.search(
            r"[\u0621-\u064A]", word) or re.search(r"[\u0660-\u0669]", word):
            return False

        # remove number from the line if there is any
        idti_line = re.sub(r"\d+", "", idti_line)
        return idti_line

def create_alignment_file(final_cvs_path, target_regions, language_code_mapping,
                          alignment_folder,training_it_folder, training_dialect_folder):
    # open the csv file and read it
    with open(final_cvs_path, "r", encoding="utf8") as f1:
        text = f1.readlines()
        next(f1, None)

        unique_standard_it = set()

        # create alignment files based on the target regions
        for target_region in target_regions:
            # create a list of tuples, each tuple contains the standard italian phrase and the phrase in the target region
            # the list is used to create the alignment file
            alignment_list = []

            # use language_code_mapping to get the language code of the target region
            language_code = language_code_mapping[target_region]

            # skip the first line
            for line in text[1:]:
                # split the line into three columns
                standard_it, phase, region = line.split("\t")
                unique_standard_it.add(standard_it)

                # if the region in the line is the target region, add the tuple to the list
                region = region.strip()
                if region == target_region:
                    alignment_list.append((standard_it, phase))
            # create the alignment file
            if not os.path.exists(alignment_folder):
                os.makedirs(alignment_folder)
            alignment_subfolder = os.path.join(alignment_folder, language_code)
            if not os.path.exists(alignment_subfolder):
                os.makedirs(alignment_subfolder)

            # FOR GIZA++: create two files, one for the standard italian phrase and one for the phrase in the target region
            # with open(os.path.join(alignment_subfolder, "standard_it"), "w", encoding="utf8") as f2:
            #     for item in alignment_list:
            #         f2.write(item[0])
            #         f2.write("\n")
            # with open(os.path.join(alignment_subfolder, "phase"), "w", encoding="utf8") as f3:
            #     for item in alignment_list:
            #         f3.write(item[1])
            #         f3.write("\n")

            # create one file that contains both the standard italian phrase and the phrase
            with open(os.path.join(alignment_subfolder, "combined"), "w", encoding="utf8") as f4:
                for item in alignment_list:
                    f4.write(item[0])
                    f4.write(" ||| ")
                    f4.write(item[1])
                    f4.write("\n")

            print("**********")
            print("alignment file for", language_code, "created")
            print("total phases:", len(alignment_list))
            print("**********\n")
            print("**********")
            print("total unique standard it:", len(unique_standard_it))
            print("**********\n")

            training_it_file = os.path.join(training_it_folder, "it.txt")
            training_dialect_file = os.path.join(training_dialect_folder,
                                                 (language_code + "_texts/"), "AA", "extracted.combined")

            # make training folder that contains the training files
            training_folder = os.path.join(alignment_subfolder, "training_data")

            # remove the training folder if it already exists
            if not os.path.exists(training_folder):
                os.makedirs(training_folder)

            # based on the length of the alignment list, extract the same number of lines from the training files
            # and save them all into one new file together
            # open the training files
            with open(training_it_file, "r", encoding="utf8") as f_it:
                with open(training_dialect_file, "r", encoding="utf8") as f_idti:
                    # skip the first line
                    next(f_idti, None)

                    it_lines = f_it.readlines()
                    idti_lines = f_idti.readlines()

                    idti_lines = idti_lines[:len(alignment_list) + 2000]
                    it_lines = it_lines[:len(alignment_list) + 2000]

                    idti_cleaned_lines = []
                    it_cleaned_lines = []
                    
                    

                    for index, idti_line in enumerate(idti_lines):
                        if idti_line == "\n" or len(idti_line.split("\t")[0].split(" ")) < 4:
                            continue
                        if check_words(idti_line) == False:
                            continue
                        else:
                            idti_line = idti_line.split("\t")[0].lower()    

                            idti_line = clean_sent(idti_line)

                            # remove number from the line if there is any
                            idti_line = re.sub(r"\d+", "", idti_line).strip().lower()
                            idti_line = re.sub(' +', ' ', idti_line)

                            if idti_line != "" and idti_line != " " and len(idti_line)>1:
                                if idti_line not in idti_cleaned_lines:
                                    idti_cleaned_lines.append(idti_line)

                    for it_line in it_lines:
                        if it_line == "\n" or len(it_line.split()) < 4:
                            continue
                        if check_words(it_line) == False:
                            continue
                        else:
                            it_line = clean_sent(it_line)

                            # remove number from the line if there is any
                            it_line = re.sub(r"\d+", "", it_line)
                            # replace double sapce
                            it_line = re.sub(' +', ' ', it_line)

                            it_line = it_line.strip().lower()
                            if it_line != "" and it_line != " " and len(it_line)>1:
                                if it_line not in it_cleaned_lines:
                                    it_cleaned_lines.append(it_line)

                    if len(idti_cleaned_lines) < len(alignment_list) or len(it_cleaned_lines) < len(alignment_list):
                        print("ERROR: not enough lines")
                        print("idti_lines:", len(idti_lines))
                        print("it_lines:", len(it_lines))
                        print("alignment_list:", len(alignment_list))
                        print("language_code:", language_code)
                        sys.exit()

                    # trim the length of each italian line to match the length of the dialect lines
                    for i in range(len(alignment_list)):
                        # if the italian line is longer than the dialect line, trim the italian line
                            idti_cleaned_lines_len = len(idti_cleaned_lines[i].split())
                            it_cleaned_lines_len = len(it_cleaned_lines[i].split())
                            # make sure italians sentences are same length as dialect sentences
                            if idti_cleaned_lines_len+10 < it_cleaned_lines_len:
                                it_cleaned_lines[i] = " ".join(it_cleaned_lines[i].split()[:idti_cleaned_lines_len])

                    # create a new file that contains all the data
                    if not os.path.exists(os.path.join(training_folder, "all")):
                        os.makedirs(os.path.join(training_folder, "all"))

                    with open(os.path.join(training_folder, "all", "train.tsv"), "w", encoding="utf8") as f7:
                        # use the length of the alignment list to determine how many lines to extract
                        for i in range(len(alignment_list)):
                            # write the lines into the new file
                            # 0 means dialect
                            # 1 means italian
                            f7.write((idti_cleaned_lines[i] + "\t" + "0" + "\n"))
                            f7.write((it_cleaned_lines[i] + "\t" + "1" + "\n"))

                    # randomly shuffle the lines in the file
                    # read the file
                    with open(os.path.join(training_folder, "all", "train.tsv"), "r", encoding="utf8") as f5:
                        lines = f5.readlines()

                    # shuffle the lines
                    random.shuffle(lines)

                    # write the lines back into the file
                    with open(os.path.join(training_folder, "all", "train.tsv"), "w", encoding="utf8") as f6:
                        f6.write(("sentence" + "\t" + "label" + "\n"))
                        for line in lines:
                            f6.write(line)


                    # copy the file to a new file
                    shutil.copyfile(os.path.join(training_folder, "all", "train.tsv"), os.path.join(training_folder, "all", "test.tsv"))

                    # create a train, dev, test file from the training file with 80% train, 10% dev, 10% test
                    # create a train file
                    # 0 means dialect
                    # 1 means italian
                    with open(os.path.join(training_folder, "train.tsv"), "w", encoding="utf8") as f8:
                        for i in range(int(len(alignment_list) * 0.8)):
                            f8.write((idti_cleaned_lines[i].split("\t")[0].strip() + "\t" + "0" + "\n"))
                            f8.write((it_cleaned_lines[i].strip() + "\t" + "1" + "\n"))

                    # create a dev file
                    with open(os.path.join(training_folder, "dev.tsv"), "w", encoding="utf8") as f9:
                        for i in range(int(len(alignment_list) * 0.8), int(len(alignment_list) * 0.9)):
                            f9.write((idti_cleaned_lines[i].split("\t")[0].strip() + "\t" + "0" + "\n"))
                            f9.write((it_cleaned_lines[i].strip() + "\t" + "1" + "\n"))

                    # create a test file
                    with open(os.path.join(training_folder, "test.tsv"), "w", encoding="utf8") as f10:
                        for i in range(int(len(alignment_list) * 0.9), len(alignment_list)):
                            f10.write((idti_cleaned_lines[i].split("\t")[0].strip() + "\t" + "0" + "\n"))
                            f10.write((it_cleaned_lines[i].strip() + "\t" + "1" + "\n"))

                    # ramdonlize all the files
                    # train
                    with open(os.path.join(training_folder, "train.tsv"), "r", encoding="utf8") as f11:
                        train_lines = f11.readlines()
                        random.shuffle(train_lines)
                    with open(os.path.join(training_folder, "train.tsv"), "w", encoding="utf8") as f12:
                        f12.write(("sentence" + "\t" + "label" + "\n"))
                        f12.write("".join(train_lines))

                    # dev
                    with open(os.path.join(training_folder, "dev.tsv"), "r", encoding="utf8") as f13:
                        dev_lines = f13.readlines()
                        random.shuffle(dev_lines)
                    with open(os.path.join(training_folder, "dev.tsv"), "w", encoding="utf8") as f14:
                        f14.write(("sentence" + "\t" + "label" + "\n"))
                        f14.write("".join(dev_lines))

                    # copy the dev file to a new file
                    shutil.copyfile(os.path.join(training_folder, "dev.tsv"), os.path.join(training_folder, "all", "dev.tsv"))

                    # test
                    with open(os.path.join(training_folder, "test.tsv"), "r", encoding="utf8") as f15:
                        test_lines = f15.readlines()
                        random.shuffle(test_lines)
                    with open(os.path.join(training_folder, "test.tsv"), "w", encoding="utf8") as f16:
                        f16.write(("sentence" + "\t" + "label" + "\n"))
                        f16.write("".join(test_lines))



def create_csv(xls_file_folder_path, final_cvs_path, target_region):
    # read every xls file in the folder and clean them
    
    all = {}
    # use tqdm to show the progress bar
    for file in tqdm.tqdm(glob.glob(os.path.join(xls_file_folder_path, "*.xls"))):
        # print(file)
        it = clean_xls(file, target_region)
        for key, value in it.items():
            # if the key is already in all, append the value to the key
            if key in all:
                # if the value is already in the key, skip it
                for v in value:
                    if v not in all[key]:
                        all[key].append(v)
            # if the key is not in all, add the key and value to all
            else:
                all[key] = value

    print("**********")
    print("total length:", len(all))

    # convert all to a dataframe where the first column is the key and the second and third columns are each value
    # in the value list which is separated by a comma. The dataframe will have 3 columns and they are
    # "standard_it", "phrase", "region" which "\t" is used to separate the columns
    final_list = []
    for key, value in all.items():
        key = key.lower()
        for v in value:
            phrase = v[0].lower()
            region = v[1]
            final_list.append((key, phrase, region))

    final_df = pd.DataFrame(final_list, columns=["standard_it", "phrase", "region"])

    # save the dataframe to a csv file and separate the columns with tab
    final_df.to_csv(final_cvs_path, sep="\t", index=False)


def main():
    target_region = ["Piemonte", "Sicilia", "Veneto", "Friuli Venezia Giulia", "Emilia Romagna", "Campania", "Taranto",
                     "Sardegna", "Liguria", "Lombardia"]
    language_code_mapping = {"Piemonte": "pms", "Sicilia": "scn", "Veneto": "vec", "Friuli Venezia Giulia": "fur",
                             "Emilia Romagna": "eml", "Campania": "nap", "Taranto": "roa_tara", "Sardegna": "sc",
                             "Liguria": "lij", "Lombardia": "lmo"}

    # all the paths
    xls_file_folder_path = "/scratch/rxie/selfexplain/my-self-exp/data/it/xls/xls_files"
    final_cvs_path = "/scratch/rxie/selfexplain/my-self-exp/data/it/xls/it_xls.csv"
    alignment_folder = "/scratch/rxie/selfexplain/my-self-exp/data/it/xls/alignment_files"
    training_it_folder = "/scratch/rxie/selfexplain/my-self-exp/data/it/Europarl_v8"
    training_dialect_folder ="/scratch/rxie/selfexplain/my-self-exp/data/it/IDTI"

    #create_csv(xls_file_folder_path, final_cvs_path, target_region)
    create_alignment_file(final_cvs_path, target_region,
                         language_code_mapping, alignment_folder, training_it_folder, training_dialect_folder)

    # run a .sh file to create the fastalign alignments
    print("**********")
    print("running fastalign...")
    os.system("sh /scratch/rxie/selfexplain/my-self-exp/scripts/run_fastAlign_folder.sh")
    print("**********")

    print("**********")
    print("creating lexicon...")
    # run create_lexicon.py to create the lexicon
    os.system("/scratch/rxie/selfexplain/self-env-4/bin/python /scratch/rxie/selfexplain/my-self-exp/preprocessing/create_lexicon.py")
    print("**********")

    print("pipline finished!")


if __name__ == "__main__":
    main()