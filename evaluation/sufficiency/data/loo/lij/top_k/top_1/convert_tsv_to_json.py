import csv
import json

def tsv_to_json(tsv_file, json_file):
    data = []
    
    with open(tsv_file, 'r', encoding='utf-8-sig') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        
        # Skip the header row if present
        next(reader)
        
        for row in reader:
            sentence = row[0]
            label = row[1]
            
            entry = {
                'sentence': sentence,
                'label': label
            }
            
            data.append(entry)
    
    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        for entry in data:
            json.dump(entry, jsonfile, ensure_ascii=False)
            jsonfile.write('\n')
        
    print(f"Conversion complete. JSON file '{json_file}' created.")


# Example usage
tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_1/train.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_1/train_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_1/test.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_1/test_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_1/dev.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_1/dev_with_parse.json'
tsv_to_json(tsv_file, json_file)

# Example usage
tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_3/train.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_3/train_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_3/test.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_3/test_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_3/dev.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_3/dev_with_parse.json'
tsv_to_json(tsv_file, json_file)

# Example usage
tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_5/train.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_5/train_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_5/test.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_5/test_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_5/dev.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/lij/top_k/top_5/dev_with_parse.json'
tsv_to_json(tsv_file, json_file)



# zh

# Example usage
tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_1/train.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_1/train_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_1/test.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_1/test_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_1/dev.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_1/dev_with_parse.json'
tsv_to_json(tsv_file, json_file)

# Example usage
tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_3/train.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_3/train_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_3/test.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_3/test_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_3/dev.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_3/dev_with_parse.json'
tsv_to_json(tsv_file, json_file)

# Example usage
tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_5/train.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_5/train_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_5/test.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_5/test_with_parse.json'
tsv_to_json(tsv_file, json_file)

tsv_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_5/dev.tsv'
json_file = '/scratch/rxie/selfexplain/my-self-exp/evluation/loo/zh/top_k/top_5/dev_with_parse.json'
tsv_to_json(tsv_file, json_file)

