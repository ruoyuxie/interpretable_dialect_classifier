import argparse
import json
from collections import OrderedDict

import torch
from transformers import AutoTokenizer, AutoConfig, AutoModel, RobertaConfig, XLNetConfig, XLMRobertaTokenizer, XLMRobertaConfig

from transformers.modeling_utils import SequenceSummary

from utils import chunks

config_dict = {'xlnet-base-cased': XLNetConfig,
               'roberta-base': RobertaConfig,
               'xlm-roberta-base':XLMRobertaConfig}

def concept_store(input_file_name, output_folder,model_name, max_concept_length, batch_size=5):
    
    # Check if CUDA is available
    if torch.cuda.is_available():
    # Use CUDA
        device = torch.device("cuda")
    else:
    # Use the CPU
        device = torch.device("cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)
    model.eval()
    # config = AutoConfig.from_pretrained(model_name)
    config = config_dict[model_name]
    sequence_summary = SequenceSummary(config)

    concept_idx = OrderedDict()
    # print("model_name =",model_name)
    idx = 0
    with open(input_file_name, 'r', encoding = "utf-8") as input_file:
        for i, line in enumerate(input_file):
            json_line = json.loads(line)
            sentence = json_line["sentence"].strip().strip(' .')
            if len(sentence.split()) <= max_concept_length:
                concept_idx[idx] = sentence
                idx += 1

    concept_tensor = []
    for batch in chunks(list(concept_idx.values()), n=batch_size):
        inputs = tokenizer(batch, padding=True, return_tensors="pt")
        for key, value in inputs.items():
            inputs[key] = value.to(device)
        outputs = model(**inputs)
        pooled_rep = sequence_summary(outputs[0])
        concept_tensor.append(pooled_rep.detach().cpu())

    concept_tensor = torch.cat(concept_tensor, dim=0)

    torch.save(concept_tensor, f'{output_folder}/concept_store.pt')
    with open(f'{output_folder}/concept_idx.json', 'w', encoding = "utf-8") as out_file:
        json.dump(concept_idx,out_file, ensure_ascii=False)

    return


def main():
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--input_train_file", "-i", default=None, type=str,
                        required=False,
                        help="The input train file")

    parser.add_argument("--output_folder", "-o", default=None, type=str, required=False,
                        help="Output folder for concept store and dict")

    parser.add_argument("--model_name", "-m", default='model_name', type=str, required=False,
                        help="Model name")

    parser.add_argument("--max_concept_len", "-l", default=5, type=int, required=False,
                        help="Max length of concept")

    args = parser.parse_args()

    concept_store(input_file_name=args.input_train_file,
                  output_folder=args.output_folder,
                  model_name=args.model_name,
                  max_concept_length=args.max_concept_len)


if __name__ == "__main__":
    main()