import os
import json
from model import XLMRBinaryClassifier
import numpy as np
from eval import *
from data_loader import *
from experiments import *
from create_human_eval_1_and_2 import *
from tqdm import tqdm

def evaluate_classifier(test_data, clf):
    # load test data
    test_texts = [d[0] for d in test_data]
    test_labels = [int(d[1]) for d in test_data]
    predictions = []
    # Evaluate classifier on test data
    for i in tqdm(range(len(test_texts))):
        input_sent = test_texts[i]
        true_label = test_labels[i]
        pred_label, proba = clf.predict(input_sent)
        predictions.append(int(pred_label))

    print("Accuracy: ", accuracy(predictions, test_labels))
    print("F1: ", f1(predictions, test_labels))
    print("Precision: ", precision(predictions, test_labels))
    print("Recall: ", recall(predictions, test_labels))

def main(lang_flag, train_path, test_path ,lexicon_silver_path, model_output_path, loo_results_path):
    data = get_train_data(train_path, lang_flag, lexicon_silver_path)

    train_texts = [d[0] for d in data]
    train_labels = [int(d[1]) for d in data]

    # count number of 1s and 0s
    print("Number of 1s in train: ", train_labels.count(1))
    print("Number of 0s in train: ", train_labels.count(0))

    # Create XLM-Roberta binary classifier
    clf = XLMRBinaryClassifier()

    # Train classifier on example data
    clf.train(train_texts, train_labels)
    #clf.save_model(model_output_path)

    #clf.load_model(model_output_path)

    # load test data
    test_data= get_test_data(test_path)
    #test_data = data

    # Evaluate classifier on test data
    evaluate_classifier(test_data, clf)


    # Evaluate contrastive_experiment
    # contrastive_experiment(train_texts, train_labels, clf)

    # Evaluate leave_one_out_experiment
    # leave_one_out_experiment_per_sent(test_data[111], clf)
    #leave_one_out_experiment_for_sentences(test_data, clf,loo_results_path)

    # extract_top_words(loo_results_path)
    # get_sample_instances(loo_results_path)


if __name__ == '__main__':
    lang_flag = "zh"

    # train_path = "/scratch/rxie/selfexplain/my-self-exp/contrastive_model/data/vec/train_with_parse.json"
    # lexicon_silver_path = "/scratch/rxie/selfexplain/my-self-exp/contrastive_model/data/vec/lexicon_silver"

    root_path = "C:\My Programs\PycharmPrograms\contrastive-classifier\sufficiency\data\loo\zh/top_k/top_5"
    lexicon_silver_path = "C:\My Programs\PycharmPrograms\contrastive-classifier\human-eval\lij\lexicon_silver"


    train_path = root_path + "/train_with_parse.json"
    test_path = root_path + "/test_with_parse.json"
    loo_results_path = root_path + "/test_loo_result_1gram.csv"
    #model_output_path = os.path.join(root_path, os.path.basename(root_path).split("/")[0] + "_model")


    model_output_path = "C:\My Programs\PycharmPrograms\contrastive-classifier\human-eval\lij\lij-model"

    if os.path.exists(model_output_path):
        print("ERROR: model exists, please rename it or delete it")
        #exit(0)

    if lang_flag == "zh":
        lexicon_silver_path = None

    main(lang_flag, train_path,test_path , lexicon_silver_path, model_output_path,loo_results_path)
