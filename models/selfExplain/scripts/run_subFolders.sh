#!/bin/bash
export TOKENIZERS_PARALLELISM=false
export MODEL_NAME=xlm-roberta-base
export DATA_FOLDER=/scratch/rxie/selfexplain/my-self-exp/data/it/xls/alignment_files
export GRAMS=1
export DE_CHUNKER=false

for dir in $DATA_FOLDER/*; do


    # echo "----------------------------------------------------------"
    # echo "--------------------preprocessing data...-----------------"
    # echo "----------------------------------------------------------"
    
    # training_data folder is inside of $dir
    export dir=$dir/training_data

    # echo $dir
    # echo $MODEL_NAME

    # python preprocessing/store_parse_trees.py \
    #     --data_dir $dir  \
    #     --tokenizer_name $MODEL_NAME  \
    #     --number_of_grams $GRAMS  \
    #     --de_chunker false

    # echo "--------------------------------------------------------"
    # echo "--------------------running model...--------------------"
    # echo "--------------------------------------------------------"
    # python model/run.py --dataset_basedir $dir \
    #                         --lr 2e-5  --max_epochs 5 \
    #                         --concept_store $dir/concept_store.pt \
    #                         --model_name $MODEL_NAME \
    #                         --topk 5 \
    #                         --gamma 0.01 \
    #                         --lamda 0.01 \

    # echo "------------------------------------------------------------"
    # echo "--------------------inferencing model...--------------------"
    # echo "------------------------------------------------------------"
    # export BEST_MODEL=$dir/checkpoints/$(ls $dir/checkpoints/ | grep ckpt | sort -n -t _ -k 3 | tail -1)

    # if [ -f "$dir/test_with_parse.json" ]; then
    #     export DEV_FILE=$dir/test_with_parse.json
    # else
    #     export DEV_FILE=$dir/dev_with_parse.json
    # fi

    # export OUTPUT_RESULT=$dir/result_$GRAMS"gram.csv"

    # echo $BEST_MODEL
    # echo $DEV_FILE
    # echo $OUTPUT_RESULT

    # python model/infer_model.py --ckpt $BEST_MODEL \
    #     --concept_map $dir/concept_idx.json \
    #     --paths_output_loc $OUTPUT_RESULT \
    #     --dev_file $DEV_FILE \
    #     --batch_size 16

    echo "------------------------------------------------------------"
    echo "--------------------calculating precision and recall...--------------------"
    echo "------------------------------------------------------------"
    export OUTPUT_RESULT=$dir/result_$GRAMS"gram.csv"
    echo $OUTPUT_RESULT

    python /scratch/rxie/selfexplain/my-self-exp/scripts/precision_recall.py $OUTPUT_RESULT

    echo "------------------------------------------------------------"


done
