import pandas as pd
import sys
import re
import nltk
import json

# DE_LABELS = {'OWL': 0, 'OFL': 1, 'HAM': 2, 'HOL': 3, 'SUD': 4, 'MKB': 5, 'DRE': 6, 'ACH': 7, 'NPR': 8, 'NNI': 9,
#                  'OVY': 10, 'OFR': 11, 'MAR': 12, 'TWE': 13, 'MON': 14, 'GRO': 15}

TOP_EXPLANATIONS = 5


def create_words_list(lang):
    lil_list = lang['lil_interpretations'].apply(lambda x: eval(x)).apply(lambda x: x[:TOP_EXPLANATIONS]).tolist()
    # for each element in lil_list, get the key of each tuple and add to a list
    words = []
    for i in range(len(lil_list)):
        for j in range(len(lil_list[i])):
            if lil_list[i][j][0] != "" and len(lil_list[i][j][0]) > 1:
                words.append(lil_list[i][j])

    return words


def get_top_n_frequncy(words, n, class_top_words):
    freq = pd.Series(words).value_counts()
    class_top_words[0] = freq[:n].to_dict()
    # print(freq[:n])


def process_csv(df, lexicon_path):
    # only keep rows that have same predicted_labels and true_labels
    df = df[df['predicted_labels'] == df['true_labels']]
    print(f"Number of entry with correct prediction: {len(df)}\n")

    # get the highest true_labels value
    num_of_classes = df.groupby(['true_labels']).max()
    print(f"Number of classes: {num_of_classes.shape[0]}\n")

    # split df into sub dataframes based on the number of classes
    df_list = []
    for i in range(num_of_classes.shape[0]):
        df_list.append(df[df['true_labels'] == i])

    # create a top_words list for each sub dataframe
    class_top_words = []
    for i in range(num_of_classes.shape[0]):
        class_top_words.append([])
        # create freq_words list, aggated_score list, and tfidf list for each sub dataframe
        freq_words = {}
        class_top_words[i].append(freq_words)

    words_lists = []
    # create a words list for each sub dataframe
    for i in range(len(df_list)):
        words_list = []
        # filter out stop words and create a words list for each sub dataframe
        words_list = create_words_list(df_list[i])
        words_lists.append(words_list)

    # if a word is appeared in both words lists, remove it from both lists
    # NOTE: when a word is very common in one list but not in the other, it will be removed, which is not good
    # deduplicate_words(words_lists)
    for i in range(len(words_lists)):
        words_list = words_lists[i]

        words_list = [word[0] for word in words_list]
        words_lists[i] = words_list

    # read lexicon file as a list of words
    with open(lexicon_path, 'r',encoding="utf-8") as f:
        lexicon = f.read().splitlines()
        # print(lexicon)
        # split the line into italian words and their corresponding dialect words
        lexicon = [line.split(' - ') for line in lexicon]
        for i in range(len(lexicon)):
            lexicon[i][1] = lexicon[i][1].split('\t')
            for j in range(len(lexicon[i][1])):
                lexicon[i][1][j] = lexicon[i][1][j].split(':')[0]

        # make lexicon into tuples
        lexicon = [(word[0], word[1]) for word in lexicon]

        class_0 = words_lists[0]
        class_1 = words_lists[1]

        # class 1 is italian, class 0 is dialect

        target_pairs = []

        # for word in lexicon:
        #     it_word = word[0]
        #     dia_words = word[1]
        #     for dia_word in dia_words:
        #         if it_word in class_1 and dia_word in class_0:
        #             target_pairs.append((it_word, dia_word))



        for word_class_1 in class_1:
            if word_class_1 in [word[0] for word in lexicon]:
                for word in lexicon:
                    if word[0] == word_class_1:
                        for word_class_0 in word[1]:
                            if word_class_0 in class_0:
                                # if (word_class_0, word_class_1) not in target_pairs:
                                target_pairs.append((word_class_0, word_class_1))
                                    # break

        print(len(target_pairs))


def main(file_path, lexicon_path):
    print("File path: ", file_path)

    # read csv file split by tab
    df = pd.read_csv(file_path, header=0, sep='\t')
    print("Number of original entry: ", len(df))

    process_csv(df, lexicon_path)


if __name__ == '__main__':
    # help message
    # if len(sys.argv) != 2:
    #     print("Usage: python tfidf.py <file path> <number of top words>")
    #     print("Example: python tfidf.py result.csv 10")
    #     exit()

    # get command line arguments for file path and number of top words
    # file_path = sys.argv[1]
    file_path = "/scratch/rxie/selfexplain/my-self-exp/data/it/xls/alignment_files/eml/training_data/result_1gram.csv"
    lexicon_path = "/scratch/rxie/selfexplain/my-self-exp/data/it/xls/alignment_files/eml/lexicon"
    main(
        file_path=file_path,
        lexicon_path=lexicon_path
    )