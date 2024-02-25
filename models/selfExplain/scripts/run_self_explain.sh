#!/bin/bash
export TOKENIZERS_PARALLELISM=false
export MODEL_NAME=xlm-roberta-base
export DATA_FOLDER=/scratch/rxie/selfexplain/my-self-exp/old_data/xlmr-de-sample-binary
export GRAMS=3
export DE_CHUNKER=false

python model/run.py --dataset_basedir $DATA_FOLDER \
                         --lr 2e-5  --max_epochs 5 \
                         --concept_store $DATA_FOLDER/concept_store.pt \
                         --model_name $MODEL_NAME \
                         --topk 5 \
                         --gamma 0.01 \
                         --lamda 0.01 \