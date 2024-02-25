import os 
import sys 
import pandas as pd

def get_precision_recall_folder(folder_path):
    # read each subfolder in the directory
    for folder in os.listdir(folder_path):

        print ("\n===============================")
        print ("Folder: ", folder)

        try:
        # read "normal_results_1gram.csv" file in each subfolder
            file_name = os.path.join(folder_path, folder, "normal_result_1gram.csv")
            df = pd.read_csv(file_name, header=0, sep='\t')
            print("Number of prediction: ", len(df))
        except:
            print("File not found")
            continue

        # get the number of class 0
        class_0 = len(df[df['true_labels'] == 0])
        print("Number of class 0: ", class_0)

        # get the number of class 1
        class_1 = len(df[df['true_labels'] == 1])
        print("Number of class 1: ", class_1)
        print (df[df['true_labels'] == 1])

        # get the number of class 0 that are predicted as class 1
        class_0_pred_1 = len(df[(df['true_labels'] == 0) & (df['predicted_labels'] == 1)])
        print("Number of class 0 that are predicted as class 1: ", class_0_pred_1)

        # get the number of class 1 that are predicted as class 0
        class_1_pred_0 = len(df[(df['true_labels'] == 1) & (df['predicted_labels'] == 0)])
        print("Number of class 1 that are predicted as class 0: ", class_1_pred_0)

        # calculate precision and recall for class 0
        precision_0 = (class_0 - class_0_pred_1) / class_0
        recall_0 = (class_0 - class_0_pred_1) / (class_0 + class_1_pred_0)
        print("Precision for class 0: ", precision_0)
        print("Recall for class 0: ", recall_0)

        # calculate precision and recall for class 1
        precision_1 = (class_1 - class_1_pred_0) / class_1
        recall_1 = (class_1 - class_1_pred_0) / (class_1 + class_0_pred_1)
        print("Precision for class 1: ", precision_1)
        print("Recall for class 1: ", recall_1)

        # calculate accuracy for the whole dataset
        accuracy = (class_0 - class_0_pred_1 + class_1 - class_1_pred_0) / (class_0 + class_1)
        print("Accuracy: ", accuracy)
        
        print ("===============================\n")

def get_precision_recall_file(file_path):
    try:
    # read "normal_results_1gram.csv" file in each subfolder
        df = pd.read_csv(file_path, header=0, sep='\t')
        print("Number of prediction: ", len(df))
    except:
        print("File not found")
        return
    
    # get the number of class 0
    class_0 = len(df[df['true_labels'] == 0])
    print("Number of class 0: ", class_0)

    # get the number of class 1
    class_1 = len(df[df['true_labels'] == 1])
    print("Number of class 1: ", class_1)
    # print (df[df['true_labels'] == 1])

    # get the number of class 0 that are predicted as class 1
    class_0_pred_1 = len(df[(df['true_labels'] == 0) & (df['predicted_labels'] == 1)])
    print("Number of class 0 that are predicted as class 1: ", class_0_pred_1)

    # get the number of class 1 that are predicted as class 0
    class_1_pred_0 = len(df[(df['true_labels'] == 1) & (df['predicted_labels'] == 0)])
    print("Number of class 1 that are predicted as class 0: ", class_1_pred_0)

    # calculate precision and recall for class 0
    precision_0 = (class_0 - class_0_pred_1) / class_0
    recall_0 = (class_0 - class_0_pred_1) / (class_0 + class_1_pred_0)
    print("Precision for class 0: ", precision_0)
    print("Recall for class 0: ", recall_0)

    # calculate precision and recall for class 1
    precision_1 = (class_1 - class_1_pred_0) / class_1
    recall_1 = (class_1 - class_1_pred_0) / (class_1 + class_0_pred_1)
    print("Precision for class 1: ", precision_1)
    print("Recall for class 1: ", recall_1)

    # calculate accuracy for the whole dataset
    accuracy = (class_0 - class_0_pred_1 + class_1 - class_1_pred_0) / (class_0 + class_1)
    print("Accuracy: ", accuracy)
    
    print ("===============================\n")


if __name__ == "__main__":
    #folder_path = sys.argv[1]
    #get_precision_recall_folder("/scratch/rxie/selfexplain/my-self-exp/data/de/pairwise/TWE")
    # get the first argument as the file path
    file_path = sys.argv[1]
    print(file_path)

    get_precision_recall_file(file_path)