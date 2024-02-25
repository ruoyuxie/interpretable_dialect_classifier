#-*- coding: utf-8 -*-
from data_loader import *
from eval import *
from tqdm import tqdm
import csv

def contrastive_experiment(data, label, model):

    predictions = []

    for sentence in data:

        original_text = sentence
        contrastive_text = ""
        lexicon = get_frmt_lexicon()[0]
        reversed_lexicon = {v: k for k, v in lexicon.items()}

        for word in original_text.split():

            if word in lexicon:
                translation = lexicon[word]
                # swap the word with its translation
                contrastive_text = (original_text.replace(word, translation))
            elif word in reversed_lexicon:
                translation = reversed_lexicon[word]
                # swap the word with its translation
                contrastive_text = (original_text.replace(word, translation))

        # compare the probability difference of the model prediction between original text with the contrastive text

        for original_text, contrastive_text in zip([original_text], [contrastive_text]):


            original_pred_label, original_proba = model.predict(original_text)
            contrastive_pred_label, contrastive_proba = model.predict(contrastive_text)

            predictions.append(int(original_pred_label))

            if original_text == contrastive_text or original_text == "" or contrastive_text == "":
                print("skipped")
                print(original_text)
                print(contrastive_text)
                print("\n")
                continue

            if abs(original_proba - contrastive_proba) > 0.2:
                print("\n")

                print("Original text: ", original_text)
                print("Original prediction: ", original_pred_label)
                print("Original probability: ", original_proba)
                print("\n")
                print("Contrastive text: ", contrastive_text)
                print("Contrastive prediction: ", contrastive_pred_label)
                print("Contrastive probability: ", contrastive_proba)
                print("\n")

                print("---------------------------------")
    # compare the predictions with the train_labels
    print("Accuracy: ", accuracy(predictions, label))
    print("F1: ", f1(predictions, label))
    print("Precision: ", precision(predictions, label))
    print("Recall: ", recall(predictions, label))
def leave_one_out_experiment_per_sent(original_sent, model):

    original_pred_label, original_proba = model.predict(original_sent)
    print(f"Original sentence: {original_sent}")
    print(f"Original sentence prediction: {original_pred_label}")
    print(f"Original sentence probability: {original_proba}")
    print("\n")

    # Split sentence into a list of words
    words = original_sent.split()

    # Perform LOO on each word in the sentence
    for i in range(len(words)):
        # Remove one word from the sentence
        left_out_word = words.pop(i)
        left_out_sentence = " ".join(words)

        # Evaluate the impact on the sentence
        # (In this example, we're just printing the left-out sentence for simplicity)
        llo_pred_label, llo_proba = model.predict(left_out_sentence)
        print(f"Left out word: {left_out_word}")
        print(f"Left out sentence: {left_out_sentence}")
        print(f"Left out sentence prediction: {llo_pred_label}")
        print(f"Left out sentence probability: {llo_proba}")
        print("\n")

        # Add the left-out word back into the sentence for the next iteration
        words.insert(i, left_out_word)

def leave_one_out_experiment_for_sentences(data, model, result_file_path):

    predictions = []
    labels = []
    results = []

    with open(result_file_path, 'w', newline='',encoding="utf-8") as result_file:
        # text file to write the results to, not csv
        writer = csv.writer(result_file, delimiter='\t')
        # write the header
        writer.writerow(["predicted_labels","true_labels", "original_sent", "lil_interpretations"])

        for original_sent, original_label in tqdm(data):
            labels.append(int(original_label))
            original_pred_label, original_proba = model.predict(original_sent)
            predictions.append(int(original_pred_label))

            # Split sentence into a list of words
            words = original_sent.split()

            # Dictionary to store highest probability difference for each word
            prob_diffs = {}

            # Perform LOO on each word in the sentence
            for i in range(len(words)):
                # Remove one word from the sentence
                left_out_word = words.pop(i)
                left_out_sentence = " ".join(words)

                # Evaluate the impact on the sentence
                llo_pred_label, llo_proba = model.predict(left_out_sentence)
                prob_diff = round((abs(original_proba - llo_proba) * 1000000),4)

                # Store highest probability difference for this word
                if left_out_word not in prob_diffs or prob_diff > prob_diffs[left_out_word]:
                    prob_diffs[left_out_word] = prob_diff

                # Add the left-out word back into the sentence for the next iteration
                words.insert(i, left_out_word)

            # Sort words by probability difference and select top five
            top_words = sorted(prob_diffs.items(), key=lambda x: x[1], reverse=True)[:5]

            # Check if all five top words have the same probability difference or if the last three top words have the same probability difference
            if len(set([x[1] for x in top_words])) == 1 or (len(top_words) >= 2 and top_words[-1][1] == top_words[-2][1] == top_words[-3][1]):
                continue  # Skip printing if the conditions are met

            # write the results to a file
            writer.writerow([original_pred_label,original_label, original_sent, top_words])
            results.append([original_pred_label,original_label, original_sent, top_words])



        print("Accuracy: ", accuracy(predictions, labels))
        print("F1: ", f1(predictions, labels))
        print("Precision: ", precision(predictions, labels))
        print("Recall: ", recall(predictions, labels))
