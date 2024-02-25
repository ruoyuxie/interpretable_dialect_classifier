import csv

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
import sys
import re
import nltk
import json
import os

# DE_LABELS = {'OWL': 0, 'OFL': 1, 'HAM': 2, 'HOL': 3, 'SUD': 4, 'MKB': 5, 'DRE': 6, 'ACH': 7, 'NPR': 8, 'NNI': 9,
#                  'OVY': 10, 'OFR': 11, 'MAR': 12, 'TWE': 13, 'MON': 14, 'GRO': 15}

TOP_EXPLANATIONS = 5

def plural_suffix_anlysis (word_list):
    en_count = 0
    et_count = 0
    # get a list of words, check every word if it ends with en or et
    for word in word_list:
        if word.endswith("en"):
            en_count += 1
        elif word.endswith("et"):
            et_count += 1
    print("total number of words: ", len(word_list))
    print("number of words ending with [en]: ", en_count)
    print("number of words ending with [et]: ", et_count)

def ofl_vs_rest (word_list):
    mik_count = 0
    dik_count = 0

    mi_count = 0
    di_count = 0

    # get a list of words, check every word if it is mik or dik or mi or di
    for word in word_list:
        if word == "mik":
            mik_count += 1
        elif word == "dik":
            dik_count += 1
        elif word == "mi":
            mi_count += 1
        elif word == "di":
            di_count += 1
    
    print("total number of words: ", len(word_list))
    print("number of words [mik]: ", mik_count)
    print("number of words [dik]: ", dik_count)
    print("number of words [mi]: ", mi_count)
    print("number of words [di]: ", di_count)

def de_vs_nl (word_list):
    
    hose_count = 0
    veur_count = 0
    zudelk_count = 0

    Huus_count = 0
    för_count = 0
    südelk_count = 0

    # if word == "hose" then hose_count += 1
    for word in word_list:
        if word == "hose" or word == "Hose":
            hose_count += 1
        elif word == "veur":
            veur_count += 1
        elif word == "zudelk":
            zudelk_count += 1
        elif word == "Huus" or word == "huus":
            Huus_count += 1
        elif word == "för":
            för_count += 1
        elif word == "südelk":
            südelk_count += 1
    
    print("total number of words: ", len(word_list))
    print("number of nl words [hose]: ", hose_count)
    print("number of nl words [veur]: ", veur_count)
    print("number of nl words [zudelk]: ", zudelk_count)
    print("---------------------------------")
    print("number of de words [Huus]: ", Huus_count)
    print("number of de words [för]: ", för_count)
    print("number of de words [südelk]: ", südelk_count)


def create_words_list (lang):

    lil_list = lang['lil_interpretations'].apply(lambda x: eval(x)).apply(lambda x: x[:TOP_EXPLANATIONS]).tolist()
    # for each element in lil_list, get the key of each tuple and add to a list
    words = []
    for i in range(len(lil_list)):
        for j in range(len(lil_list[i])):
            if lil_list[i][j][0] != "" and len(lil_list[i][j][0]) > 1:
                words.append(lil_list[i][j])

    return words

def get_top_n_frequncy (words,n, class_top_words):
    freq = pd.Series(words).value_counts()
    class_top_words[0] = freq[:n].to_dict()
    # print(freq[:n])
 
 
def get_top_n_tfidf (doc,top_n,class_top_words_tfitf,ngram_range):
    # tfIdfVectorizer = TfidfVectorizer(use_idf=True)
    # tfIdf = tfIdfVectorizer.fit_transform(doc)
    # df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
    # df = df.sort_values('TF-IDF', ascending=False)
    # print(df.head(25))


    # Getting trigrams 
    vectorizer = CountVectorizer(ngram_range = (ngram_range,ngram_range))
    X1 = vectorizer.fit_transform(doc) 
    features = (vectorizer.get_feature_names_out())
    #print("\n\nFeatures : \n", features)
    #print("\n\nX1 : \n", X1.toarray())
    
    # Applying TFIDF
    vectorizer = TfidfVectorizer(ngram_range = (ngram_range,ngram_range))
    X2 = vectorizer.fit_transform(doc)
    scores = (X2.toarray())
    #print("\n\nScores : \n", scores)
    
    # Getting top ranking features
    sums = X2.sum(axis = 0)
    data1 = []
    for col, term in enumerate(features):
        data1.append( (term, sums[0,col] ))
    ranking = pd.DataFrame(data1, columns = ['term','rank'])
    words = (ranking.sort_values('rank', ascending = False))
    # make words and their scores to list
    words = words.values.tolist()
    
    # update class_top_words
    # make eacch element to be a tuple
    # only keep the top n words
    for i in range(len(words)):
        # round the score to 3 digits
        words[i][1] = round(words[i][1],3)
        class_top_words_tfitf[2][words[i][0]] = words[i][1]
        if i == top_n:
            break
 

def get_top_aggated_score (word_list,n,class_top_words):
    aggated_score = {}
    for word in word_list:
        if word[0] in aggated_score:
            aggated_score[word[0]] += abs(word[1])
        else:
            aggated_score[word[0]] = abs(word[1])

    aggated_score = sorted(aggated_score.items(), key=lambda x: x[1], reverse=True)

    for i in range(n):
        # only print last 6 digits of the score
        # print(f"{aggated_score[i][0]}\t{aggated_score[i][1]:.6f}")
        # only print last 6 digits of the score
        class_top_words[aggated_score[i][0]] = aggated_score[i][1]
        

def print_top_words(class_top_words,top_n, scores):

    for i in range(len(class_top_words)):
        print("*"*20 +  " class "+ str(i) +" " + "*"*20)

        print(f"Top {top_n} tokens by frequency: ")
        n = 0
        for word in class_top_words[i][0]:
            # only print first top_n words
            if n < top_n:
                if scores == True:
                    print(f"{word}\t{class_top_words[i][0][word]}")
                else:
                    print(f"{word}")
                n += 1  
            else:
                break
        
        print(f"\nTop {top_n} tokens by aggated score: ")
        n = 0
        for word in class_top_words[i][1]:
            # only print first top_n words
            if n < top_n:
                if scores == True:
                    print(f"{word}\t{class_top_words[i][1][word]:.3f}")
                else:
                    print(f"{word}")
                n += 1
            else:
                break
        
        print(f"\nTop {top_n} tokens by tfidf: ")
        n = 0
        for word in class_top_words[i][2]:
            if n < top_n:
                if scores == True:
                    print(f"{word}\t{class_top_words[i][2][word]}")
                else:
                    print(f"{word}")
                n += 1
            else:
                break

        print("\n")

def dup_check(class_top_words):
    dupcheck0 = []
    # if a word is appeared in the top words list of all classes, remove it from both lists
    for i in range(len(class_top_words)):
        for j in range(len(class_top_words)):
            if i != j:
                for word in class_top_words[i][0]:
                    if word in class_top_words[j][0]:
                        dupcheck0.append(word)
    
    for i in range(len(class_top_words)):
        for word in dupcheck0:
            if word in class_top_words[i][0]:
                class_top_words[i][0].pop(word)

    dupcheck1 = []
    for i in range(len(class_top_words)):
        for j in range(len(class_top_words)):
            if i != j:
                for word in class_top_words[i][1]:
                    if word in class_top_words[j][1]:
                        dupcheck1.append(word)
    
    for i in range(len(class_top_words)):
        for word in dupcheck1:
            if word in class_top_words[i][1]:
                class_top_words[i][1].pop(word)


    dupcheck2 = []
    for i in range(len(class_top_words)):
        for j in range(len(class_top_words)):
            if i != j:
                for word in class_top_words[i][2]:
                    if word in class_top_words[j][2]:
                        dupcheck2.append(word)
    
    for i in range(len(class_top_words)):
        for word in dupcheck2:
            if word in class_top_words[i][2]:
                class_top_words[i][2].pop(word)

def find_strong_indicators (gt, json_file,top_n):


    def get_most_frequent_words(words,top_n):
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_word_count[:top_n]

    gt_class_0 = gt[0]
    gt_class_1 = gt[1]
    words_class_0 = []
    words_class_1 = []

    with open(json_file, 'r', encoding = "utf-8") as input_file:
        for k, line in enumerate(input_file):
            json_line = json.loads(line)
            sentence = json_line["sentence"]
            label = json_line["label"]
            words = sentence.split()

            if label == "0":
                for gt_word in gt_class_0:
                    if gt_word in words:
                        for w in words:
                            if w != gt_word:
                                words_class_0.append(w)

            elif label == "1":
                for gt_word in gt_class_1:
                    if gt_word in words:
                        for w in words:
                            if w != gt_word:
                                words_class_1.append(w)

    print("*" * 50)
    print("Ground Truth Class 0: ", gt_class_0)
    print("Ground Truth Class 1: ", gt_class_1)
    print("number of Class 0 words: ", len(words_class_0))
    print("number of Class 1 words: ", len(words_class_1))
    print("*" * 50)

    class_zero_words_with_freq = get_most_frequent_words(words_class_0,top_n)
    class_one_words_with_freq = get_most_frequent_words(words_class_1,top_n)

    def deduplicate_words(words_class_0, words_class_1, top_n):
        class_zero_words_with_freq = get_most_frequent_words(words_class_0, top_n * 3)
        class_one_words_with_freq = get_most_frequent_words(words_class_1, top_n * 3)

        class_zero_words = [pair[0] for pair in class_zero_words_with_freq]
        class_one_words = [pair[0] for pair in class_one_words_with_freq]

        # check what are the overlapping words in class 0 and class 1
        overlap = []
        for word in class_zero_words:
            if word in class_one_words:
                overlap.append(word)

        remove_class_zero_words = []
        remove_class_one_words = []

        # remove the overlapping words from class 0 and class 1
        for pair in class_zero_words_with_freq:
            word = pair[0]
            if word in overlap:
                remove_class_zero_words.append(pair)
        for pair in class_one_words_with_freq:
            word = pair[0]
            if word in overlap:
                remove_class_one_words.append(pair)

        for pair in remove_class_zero_words:
            class_zero_words_with_freq.remove(pair)
        for pair in remove_class_one_words:
            class_one_words_with_freq.remove(pair)

        return class_zero_words_with_freq, class_one_words_with_freq

    # if dedup is needed:
    class_zero_words_with_freq, class_one_words_with_freq = deduplicate_words(words_class_0,words_class_1,top_n)


    # get the most frequent words in class 0
    print(f"The top {top_n} strong indicators in class 0:")
    for i in range(top_n):
        # print it in the format of word: frequency
        print(class_zero_words_with_freq[i][0],":",class_zero_words_with_freq[i][1])
    print("*"*50)


    # get the most frequent words in class 1
    print(f"The top {top_n} strong indicators in class 1:")
    for i in range(top_n):
        # print it in the format of word: frequency
        print(class_one_words_with_freq[i][0],":",class_one_words_with_freq[i][1])
    print("*"*50)


def get_idti_lexicon(json_file_path):
    # get the base path of the json file, which is last and second last folder
    if "all" in json_file_path:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(json_file_path)))
    else:
        base_path = os.path.dirname(os.path.dirname(json_file_path))
    lexicon_silver_path = os.path.join(base_path, "lexicon_silver")

    lexicon = {}

    # read the lexicon_silver file
    with open(lexicon_silver_path, 'r', encoding="utf-8") as input_file:
        lexicon_silver = input_file.readlines()
        # split the lines into italian and dialect words by " - "
        lexicon_silver = [line.split(" - ") for line in lexicon_silver]
        for line in lexicon_silver:
            # remove the newline character
            line[1] = line[1].replace("\n", "")
            lexicon[line[0]] = line[1]

    return lexicon

def process_csv(print_sents_with_gt,strong_indicator,lang_flag,original_tsv_file_path,df,top_n, ngram_range, scores, json_file):

    # only keep rows that have same predicted_labels and true_labels
    df = df[df['predicted_labels'] == df['true_labels']]
    print(f"Number of entry with correct prediction: {len(df)}\n" )

    # get the highest true_labels value
    num_of_classes = df.groupby(['true_labels']).max()
    print(f"Number of classes: {num_of_classes.shape[0]}\n")

    # split df into sub dataframes based on the number of classes
    df_list = []
    for i in range(num_of_classes.shape[0]):
        df_list.append(df[df['true_labels'] == i])

    tfitf_doc = []
    # create a tfitf_doc list for each sub dataframe
    for i in range(num_of_classes.shape[0]):
        # each doc is a list of words from lil_interpretations, which is a list of words from each row without scores
        doc = []
        for row in df_list[i]['lil_interpretations']:
            row = row.replace('[','').replace(']','').replace('\'','').replace(' ','')
            words = row.split(',')

            # Extract the words and add them to a list
            word_list = []
            for word in words:
                word = word.replace('(', '').replace(')', '').split('-')[0]
                word_list.append(word)

            # Create the sentence by joining the words
            sentence = ' '.join(word_list).strip()
            doc.append(sentence)

        tfitf_doc.append(doc)


    # create a top_words list for each sub dataframe
    class_top_words = []
    for i in range(num_of_classes.shape[0]):
        class_top_words.append([])
        # create freq_words list, aggated_score list, and tfidf list for each sub dataframe
        freq_words = {}
        aggated_score = {}
        tfidf_words = {}  
        class_top_words[i].append(freq_words)
        class_top_words[i].append(aggated_score)
        class_top_words[i].append(tfidf_words)
        
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

    if lang_flag == 'zh':
        _, lexicon = get_frmt_lexicon()
    elif lang_flag == 'pt':
        lexicon,_  = get_frmt_lexicon()
    elif lang_flag == 'it':
        lexicon = get_idti_lexicon(json_file)

    if strong_indicator == True:
        # make a list a keys and values
        keys = list(lexicon.keys())
        values = list(lexicon.values())
        # first element is keys, second element is values
        exp_list = [keys, values]
        find_strong_indicators(exp_list, json_file,top_n)


    count_words_in_exp = [{},{}]
    top_n = top_n * 2
    for i in range(len(words_lists)):

        words_list = words_lists[i]

        get_top_aggated_score(words_list, top_n, class_top_words[i][1])
        
        words_list = [word[0] for word in words_list]

        # compare with gold lables
        #print(f"class {i}:")
        #plural_suffix_anlysis(words_list)
        #ofl_vs_rest(words_list)
        #de_vs_nl(words_list)
        
        # evaluate lexicons
        # ZH: i=0 is cn, 1 is tw
        # PT: i=0 is pt, 1 is br

        print(f"class {i}:")
        for word in lexicon:
            # count the number of times words appear in the lexicon
            if word in words_list:
                count = words_list.count(word)
                print(f"{word}: {count}")
                count_words_in_exp[i][word] = count
            elif not word in count_words_in_exp:
                print(f"{word}: 0")
                count_words_in_exp[i][word] = 0
        print("*" * 20)

        for word in lexicon:
            word_translation = lexicon[word]
            # count the number of times words appear in the word's value
            if word_translation in words_list:
                count = words_list.count(word_translation)
                print(f"{word_translation}: {count}")
                count_words_in_exp[i][word_translation] = count
            elif not word_translation in count_words_in_exp:
                print(f"{word_translation}: 0")
                count_words_in_exp[i][word_translation] = 0
        print("*" * 20)

        get_top_n_frequncy(words_list, top_n, class_top_words[i][0])

        class_top_words[i][0] = class_top_words[i][0][0]

        get_top_n_tfidf(tfitf_doc[i], top_n, class_top_words[i], ngram_range)

    print("Original TSV file:")
    original_tsv_file = original_tsv_file_path
    # read the file
    with open(original_tsv_file, 'r',encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='\t')
        # skip the header
        next(reader)

        doc = []
        # concatenate all rows into one string
        for row in reader:
            line = row[0
            ]
            words = line.split()
            for word in words:
                word = word.strip()
                if word != "":
                    doc.append(word)

        count_words_in_text = {}
        # count the number of times lexicon words appear in the string
        for word in lexicon:
            if word in doc:
                count = doc.count(word)
                print(f"{word}: {count}")
                count_words_in_text[word] = count
            else:
                print(f"{word}: 0")
                count_words_in_text[word] = 0
        print("*" * 20)
        for word in lexicon:
            word_translation = lexicon[word]
            if word_translation in doc:
                count = doc.count(word_translation)
                print(f"{word_translation}: {count}")
                count_words_in_text[word_translation] = count
            else:
                print(f"{word_translation}: 0")
                count_words_in_text[word_translation] = 0
        print("*" * 20)

    print("PR:")
    # calculate PR for each word. PR is calculated based on the occurance of a word in the exp devided by the occurance of the word in the text
    for list_words in count_words_in_exp:
        print("\n" * 20, "new class", "*" * 20, "\n")
        for exp_word in list_words:

            exp_count = list_words[exp_word]
            text_count = count_words_in_text[exp_word]
            if text_count != 0:
                pr = exp_count / text_count
                # only keep last 3 digits
                pr = round(pr, 3)
                print(f"{exp_word}: {pr}")
            else:
                print(f"{exp_word}: 0")

        print("*" * 20)

    top_n = int(top_n / 2)
    dup_check(class_top_words)

    # find sentences that contains top words
    if json_file is not None and print_sents_with_gt == True:
        find_sentences(class_top_words, json_file,top_n)
    else:
        #print top words for each class
        # for c in class_top_words:
        #     print("current class:")
        #     print("freq_words: ", c[0])
        #     print("aggated_score: ", c[1])
        #     print("tfidf_words: ", c[2])
        #     print("*"*50)
        print_top_words(class_top_words, top_n, scores)
        print("-"*50)


def get_frmt_lexicon():

    # Format: English: (Simp-CN, Simp-TW, Trad-TW, Trad-CN)
    orginal_zh_terms = {
        "Pineapple": ("菠萝", "凤梨", "鳳梨", "菠蘿"),
        "Computer mouse": ("鼠标", "滑鼠", "滑鼠", "鼠標"),
        # Original source had CN:牛油果, but translator used 鳄梨.
        # "Avocado": ("鳄梨", "酪梨", "酪梨", "鱷梨"),
        "Band-Aid": ("创可贴", "OK绷", "OK繃", "創可貼"),
        "Blog": ("博客", "部落格", "部落格", "博客"),
        "New Zealand": ("新西兰", "纽西兰", "紐西蘭", "新西蘭"),
        "Printer (computing)": ("打印机", "印表机", "印表機", "打印機"),
        # Original source has TW:月臺, but translator used 月台.
        "Railway platform": ("站台", "月台", "月台", "站台"),
        "Roller coaster": ("过山车", "云霄飞车", "雲霄飛車", "過山車"),
        "Salmon": ("三文鱼", "鲑鱼", "鮭魚", "三文魚"),
        "Shampoo": ("洗发水", "洗发精", "洗髮精", "洗髮水"),
        # From Wikipedia page "Software testing"
        "Software": ("软件", "软体", "軟體", "軟件"),
        "Sydney": ("悉尼", "雪梨", "雪梨", "悉尼"),

        # The following two are excluded because they underpin the first 100
        # lexical exemplars used for priming the models.
        # "Flip-flops": ("人字拖", "夹脚拖", "夾腳拖", "人字拖"),
        "Paper clip": ("回形针", "回纹针", "迴紋針", "回形針")
    }

    # Portuguese terms.
    # Format: English: (BR, PT)
    # The Portuguese corpus is lowercased before matching these terms.
    orginal_pt_terms = {
        #"Bathroom": ("banheiro", "casa de banho"),
        # Original source had "pequeno almoço" but translator used "pequeno-almoço".
        #"Breakfast": ("café da manhã", "pequeno-almoço"),
        "Bus": ("ônibus", "autocarro"),
        "Cup": ("xícara", "chávena"),
        "Computer mouse": ("mouse", "rato"),
        #"Drivers license": ("carteira de motorista", "carta de condução"),
        # From Wikipedia page "Ice cream sandwich"
        "Ice cream": ("sorvete", "gelado"),
        "Juice": ("suco", "sumo"),
        "Mobile phone": ("celular", "telemóvel"),
        "Pedestrian": ("pedestre", "peão"),
        # From Wikipedia page "Pickpocketing"
        #"Pickpocket": ("batedor de carteiras", "carteirista"),
        "Pineapple": ("abacaxi", "ananás"),
        "Refrigerator": ("geladeira", "frigorífico"),
        "Suit": ("terno", "fato"),
        "Train": ("trem", "comboio"),
        "Video game": ("videogame", "videojogos"),

        # Terms updated after original selection.

        # For BR, replaced "menina" (common in speech) with "garota" (common in
        # writing, matching the human translators.
        "Girl": ("garota", "rapariga"),

        # Replace original "Computer monitor": ("tela de computador", "ecrã") with
        # the observed use for just screen:
        "Screen": ("tela", "ecrã"),

        # Terms excluded.

        # The following three are excluded because they underpin the first 100
        # lexical exemplars used for priming the models.
        "Gym": ("academia", "ginásio"),
        "Stapler": ("grampeador", "agrafador"),
        #"Nightgown": ("camisola", "camisa de noite"),

        # The following are excluded for other reasons:

        # BR translator primarily used 'comissário de bordo' and hardly ever
        # 'aeromoça'. PT translator used 'comissários/assistentes de bordo' or just
        # 'assistentes de bordo' Excluding the term as low-signal for now.
        ## "Flight attendant": ("aeromoça", "comissário ao bordo"),

        # Both regions' translators consistently used "presunto", so the term has
        # low signal.
        ## "Ham": ("presunto", "fiambre"),
    }

    lexicon = {}
    pt_lexicon = {}

    # for each language, create a dictionary of terms
    for orginal_terms in [orginal_zh_terms, orginal_pt_terms]:
        for term, translations in orginal_terms.items():
            # if it's chinese
            if len(translations) == 4:
               # only care about Simp-CN and Trad-TW
                lexicon[translations[0]] = translations[2]
            else:
                # only care about BR and PT
                pt_lexicon[translations[0]] = translations[1]

    return lexicon, pt_lexicon

def find_sentences (top_words,json_file,top_n):

    # create a set to store unquie words
    for i in range(len(top_words)):
        print(f"class {i}:")
        for j in range(len(top_words[i])):
            current_list = ""
            freq_words = 0
            aggated_score = 1
            tfidf_words = 2  
            if j == freq_words:
                print("freq_words list:")
                current_list = "freq_words"
            elif j == aggated_score:
                print("aggated_score list:")
                current_list = "aggated_score"
            elif j == tfidf_words:
                print("tfidf_words list:")
                current_list = "tfidf_words"
            for index ,word in enumerate(top_words[i][j]):
                if index > top_n:
                    break
                with open(json_file, 'r', encoding = "utf-8") as input_file:
                    for k, line in enumerate(input_file):
                        json_line = json.loads(line)
                        sentence = json_line["sentence"]
                        if " "+ word + " " in sentence:
                            print(f"class {i}, top {current_list}, [{word}]: {sentence}")

def process_tsv(df,top_n, ngram_range,scores):
    # find the top words for each class in the raw tsv file
    de_stop_words = []
    du_stop_words = []  
    with open('/scratch/rxie/selfexplain/my-self-exp/scripts/de_stopwords.txt', 'r') as f:
        for line in f:
            de_stop_words.append(line.strip())
    
    # read de_stopwords.txt and add to stop_words
    with open('/scratch/rxie/selfexplain/my-self-exp/scripts/du_stopwords.txt', 'r') as f1:
        for line in f1:
            du_stop_words.append(line.strip())
    
    stop_words = de_stop_words + du_stop_words

    # get the highest true_labels value
    num_of_classes = df.groupby(['label']).max()

    df_list = []
    for i in range(num_of_classes.shape[0]):
        df_list.append(df[df['label'] == i])

    class_top_words = []
    for i in range(num_of_classes.shape[0]):
        class_top_words.append([])
        # create freq_words list, aggated_score list, and tfidf list for each sub dataframe
        freq_words = {}
        aggated_score = {}
        tfidf_words = {}  
        class_top_words[i].append(freq_words)
        class_top_words[i].append(aggated_score)
        class_top_words[i].append(tfidf_words)
    
    top_n = top_n * 2
    for i in range(len(df_list)):

        words_list = []
        # create a words list for each sub dataframe by adding all the words in each sentence
        for j in range(len(df_list[i])):
            sent = df_list[i]['sentence'].iloc[j]
            # remove punctuations
            sent = re.sub(r'[^\w\s]','',sent)
            # remove stopwords
            sent = " ".join([word for word in sent.split() if word not in stop_words])
            
            words_list.extend(sent.split())

        get_top_n_frequncy(words_list, top_n, class_top_words[i][0])

        class_top_words[i][0] = class_top_words[i][0][0]

        doc = " ".join(words_list)

        get_top_n_tfidf([doc], top_n, class_top_words[i], ngram_range)

        
    dup_check(class_top_words)

    # print top words for each class
    print_top_words(class_top_words, int(top_n / 2), scores)

def process_json(file_path,top_n, ngram_range,scores):
    total_words = []

    class0_words = []
    class1_words = []

    with open(file_path, 'r', encoding = "utf-8") as input_file:
        for k, line in enumerate(input_file):
            json_line = json.loads(line)
            sentence = json_line["sentence"]

            # for word in sentence.split():
            #     total_words.append(word)

            label = json_line["label"]
            if label == "0":
                for word in sentence.split():
                    class0_words.append(word)
            elif label == "1":
                for word in sentence.split():
                    class1_words.append(word)



    # print("\n"+"*"*50)
    # print("Number of words in total: ", len(total_words))
    # print("*"*50 + "\n")

    # print("plural suffix analysis in total:")
    # plural_suffix_anlysis(total_words)
    # print("*"*50 + "\n")

    # print("OFL vs. Non-OFL analysis in total:")
    # ofl_vs_rest(total_words)
    # print("*"*50 + "\n")

    # print("DE vs NL analysis in total:")
    # de_vs_nl(total_words)
    # print("*"*50 + "\n")


    print("\n"+"*"*50)
    print("Number of words in class 0: ", len(class0_words))
    print("Number of words in class 1: ", len(class1_words))
    print("*"*50 + "\n")

    print("\n"+"*"*50)
    print("Number of words in class 0: ", len(class0_words))
    print("Number of words in class 1: ", len(class1_words))
    print("*"*50 + "\n")

    print("plural suffix analysis in class 0:")
    plural_suffix_anlysis(class0_words)
    print("\n plural suffix analysis in class 1:")
    plural_suffix_anlysis(class1_words)
    print("*"*50 + "\n")


    print("OFL vs NON-OFL analysis in class 0:")
    ofl_vs_rest(class0_words)
    print("\n OFL vs NON-OFL analysis in class 1:")
    ofl_vs_rest(class1_words)
    print("*"*50 + "\n")

    print("DE vs NL analysis in class 0:")
    de_vs_nl(class0_words)
    print("\n DE vs NL analysis in class 1:")
    de_vs_nl(class1_words)
    print("*"*50 + "\n")


def main(print_sents_with_gt,strong_indicator, lang_flag,main_file_path,top_n,print_scores, json_file,original_tsv_file_path):
    
    print ("File path: ", main_file_path)

    # read csv file split by tab
    df = pd.read_csv(main_file_path, header=0, sep='\t')
    print("Number of original entry: ", len(df))
    

    if "csv" in main_file_path:
        # read the file name
        file_name = main_file_path.split('/')[-1]
        # get the number of grams from the file name (eg== : result_2gram.csv)
        ngram_range = int(file_name.split('_')[-1].split('gram')[0])


        process_csv(print_sents_with_gt,strong_indicator,lang_flag,original_tsv_file_path,df, top_n, ngram_range,print_scores, json_file)

    elif "tsv" in main_file_path:
        ngram_range = 1
        process_tsv(df, top_n, ngram_range,print_scores)
    
    elif "json" in main_file_path:
        ngram_range = 1
        process_json(main_file_path, top_n, ngram_range,print_scores)


if __name__ == '__main__':

    # help message
    # if len(sys.argv) != 2:
    #     print("Usage: python tfidf.py <file path> <number of top words>")
    #     print("Example: python tfidf.py result.csv 10")
    #     exit()

    # get command line arguments for file path and number of top words
    #file_path = sys.argv[1]
    exp_file_path = "data/all/zh/result_1gram.csv"
    original_tsv_file_path = "data/all/zh/test.tsv"
    json_file = "data/all/zh/test_with_parse.json"

    idti_data = True

    if idti_data:
        folder = "/scratch/rxie/selfexplain/my-self-exp/data/it/xls/alignment_files"
        for lang in os.listdir(folder):
            lang = os.path.join(lang,"training_data","all")

            exp_file_path = os.path.join(folder, lang, "result_1gram.csv")
            original_tsv_file_path = os.path.join(folder, lang, "test.tsv")
            json_file = os.path.join(folder, lang, "test_with_parse.json")

            print("Processing file: ", exp_file_path)
            # check the input exp_file_path to see if input is zh for frmt data

            lang_flag = "it"
            strong_indicator = True
            print_sents_with_gt = False
            
            main(
            main_file_path=exp_file_path,
            original_tsv_file_path=original_tsv_file_path,
            lang_flag=lang_flag,
            top_n=20,
            print_scores=True,
            strong_indicator=strong_indicator,
            json_file=json_file,
            print_sents_with_gt=print_sents_with_gt
            )
    else:
    

    
        # check the input exp_file_path to see if input is zh for frmt data
        lang_flag = ""
        if "zh" in exp_file_path:
            zh = "zh"

        strong_indicator = True
        print_sents_with_gt = False
        
        main(
        main_file_path=exp_file_path,
        original_tsv_file_path=original_tsv_file_path,
        lang_flag=lang_flag,
        top_n=20,
        print_scores=True,
        strong_indicator=strong_indicator,
        json_file=json_file,
        print_sents_with_gt=print_sents_with_gt
        )