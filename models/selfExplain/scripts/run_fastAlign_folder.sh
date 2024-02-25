export FOLDER_PATH=/scratch/rxie/selfexplain/my-self-exp/data/it/xls/alignment_files/
cd /scratch/rxie/fast_align/fast_align/build

# for each subfolder in the folder path, run the following command
for f in $FOLDER_PATH*; do

    export input_file=$f/combined
    export result_file=$f/combined.out


    ./fast_align -i $input_file -d -o -v > $result_file


done

