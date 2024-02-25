import csv
from collections import Counter
import random
import ast

def extract_top_words(file_path):
    top_words = {'class_0': [], 'class_1': []}

    with open(file_path, 'r', encoding='utf-8') as result_file:
        reader = csv.reader(result_file, delimiter='\t')
        next(reader)  # skip header row

        for row in reader:
            words = [w[0] for w in eval(row[3])]
            label = int(row[0])
            top_words[f'class_{label}'].extend(words)

    # Get unique top words for each class
    unique_top_words = {'class_0': set(top_words['class_0']), 'class_1': set(top_words['class_1'])}

    # Remove any words that appear in both classes
    common_words = unique_top_words['class_0'] & unique_top_words['class_1']
    unique_top_words['class_0'] -= common_words
    unique_top_words['class_1'] -= common_words

    # Get top 20 most frequent top words for each class, including any that were excluded due to being present in both classes
    top_20_words = {'class_0': [], 'class_1': []}
    for label in ['class_0', 'class_1']:
        top_word_counts = Counter(top_words[label])
        top_word_freq = top_word_counts.most_common(40)
        top_word_freq = [w for w in top_word_freq if w[0] not in common_words][:20]
        top_20_words[label] = [w[0] for w in top_word_freq]

    for i in range(len(top_20_words)):
        print("Top 20 words for class ", i)
        class_name = "class_" + str(i)
        # print(top_20_words[class_name])
        for word in top_20_words[class_name]:
            print(word)
        print("\n")


def get_sample_instances (result_file_path):
    class_0_results = {}
    class_1_results = {}

    with open(result_file_path, 'r', newline='', encoding="utf-8") as result_file:
        reader = csv.reader(result_file, delimiter='\t')
        next(reader) # skip header
        for row in reader:
            pred_label = int(row[0])
            sentence = row[2]
            top_words_list = ast.literal_eval(row[3])
            top_words_only = [word for word, prob in top_words_list]

            if pred_label == 0:
                if sentence not in class_0_results and 30 > len(sentence.split()) > 3:
                    class_0_results[sentence] = top_words_only[:3]
            elif pred_label == 1:
                if sentence not in class_1_results and 20 > len(sentence.split()) > 4:
                    class_1_results[sentence] = top_words_only[:3]

    # Get a random sample of 12 sentences from class 0, the length of the sample has to be greater than the 3
    class_0_sample = random.sample(list(class_0_results.items()), 25)

    # Get a random sample of 13 sentences from class 1
    class_1_sample = random.sample(list(class_1_results.items()), 25)

    print("\nclass_0_sample:")
    # print the combined sample in the format of "top_words => sentence"
    for sentence, top_words in class_0_sample:
        print(", ".join(top_words), ", ", sentence)

    print("\nclass_1_sample:")
    for sentence, top_words in class_1_sample:
        print(", ".join(top_words), ", ", sentence)
