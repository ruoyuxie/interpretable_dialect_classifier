#!/bin/bash
export TOKENIZERS_PARALLELISM=false
export MODEL_NAME=xlm-roberta-base
export DATA_FOLDER=/scratch/rxie/selfexplain/my-self-exp/old_data/xlmr-de-sample-binary
export GRAMS=3
export DE_CHUNKER=false

# BEST_MODEL is $DATA_FOLDER + the higest val_acc_epoch in the checkpoint folder
export BEST_MODEL=$DATA_FOLDER/checkpoints/$(ls $DATA_FOLDER/checkpoints/ | grep ckpt | sort -n -t _ -k 3 | tail -1)

# if $DATA_FOLDER has test_with_parse.json, then use it as dev_file
if [ -f "$DATA_FOLDER/test_with_parse.json" ]; then
    export DEV_FILE=$DATA_FOLDER/test_with_parse.json
else
    export DEV_FILE=$DATA_FOLDER/dev_with_parse.json
fi

# OUTPUT_RESULT file is $DATA_FOLDER + $GRAMS + gram.csv
export OUTPUT_RESULT=$DATA_FOLDER/result_$GRAMS"gram.csv"

echo $BEST_MODEL
echo $DEV_FILE
echo $OUTPUT_RESULT

python model/infer_model.py --ckpt $BEST_MODEL \
      --concept_map $DATA_FOLDER/concept_idx.json \
      --paths_output_loc $OUTPUT_RESULT \
      --dev_file $DEV_FILE \
      --batch_size 16
