#!/bin/bash
export TOKENIZERS_PARALLELISM=false
export MODEL_NAME=xlm-roberta-base
export DATA_FOLDER=/scratch/rxie/selfexplain/my-self-exp/old_data/xlmr-de-sample-binary
export GRAMS=3
export DE_CHUNKER=false

python preprocessing/store_parse_trees.py \
      --data_dir $DATA_FOLDER  \
      --tokenizer_name $MODEL_NAME  \
      --number_of_grams $GRAMS  \
      --de_chunker $DE_CHUNKER