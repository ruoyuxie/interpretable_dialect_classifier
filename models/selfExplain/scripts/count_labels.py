import os
import json
import sys

def count_labels(folder_name):
    # Step 3: Find the JSON files in the folder
    train_file_path = os.path.join(folder_name, 'train_with_parse.json')
    test_file_path = os.path.join(folder_name, 'test_with_parse.json')

    # Step 4: read if line by line
    train_data = []
    with open(train_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            train_data.append(json.loads(line))

    test_data = []
    with open(test_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            test_data.append(json.loads(line))


    # Step 5: Count the labels in the JSON files
    train_labels = {}
    for item in train_data:
        label = item['label']
        train_labels[label] = train_labels.get(label, 0) + 1

    test_labels = {}
    for item in test_data:
        label = item['label']
        test_labels[label] = test_labels.get(label, 0) + 1

    return train_labels, test_labels

folder_name = ""
# take user input as the folder name
if len(sys.argv) > 1:
    folder_name = sys.argv[1]


train_labels, test_labels = count_labels(folder_name)

print("Train Labels:")
for label, count in train_labels.items():
    print(f"{label}: {count}")

print("\nTest Labels:")
for label, count in test_labels.items():
    print(f"{label}: {count}")
