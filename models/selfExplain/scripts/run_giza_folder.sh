# ./plain2snt.out /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-clean-a /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-j

# ./snt2cooc.out /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-clean-a.vcb /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-j.vcb /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-clean-a_300-j.snt > /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/corp.cooc

# ./GIZA++ -S /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-clean-a.vcb -T /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-j.vcb -C /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-clean-a_300-j.snt -CoocurrenceFile /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/corp.cooc -outputpath /scratch/rxie/giza++/giza-pp/giza-out/ainu-ja

# python ../giza-output-process.py /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-clean-a /scratch/rxie/giza++/giza-pp/giza-data/aiun-ja/300-j /scratch/rxie/giza++/giza-pp/giza-out/ainu-ja/2022-10-18.003145.rxie.AA3.final > ../clean-a-j.out

export FOLDER_PATH=/scratch/rxie/selfexplain/my-self-exp/data/it/xls/alignment_files/
export OUTPUT_PATH=/scratch/rxie/selfexplain/my-self-exp/data/it/xls/alignment_output/
cd /scratch/rxie/giza++/giza-pp/GIZA++-v2

mkdir -p $OUTPUT_PATH

# for each subfolder in the folder path, run the following command
for f in $FOLDER_PATH*; do

    #create output folder
    mkdir -p $OUTPUT_PATH$(basename $f)

    export phase=$f/phase
    export standard_it=$f/standard_it
    export phase_standard_it=$f/phase_standard_it
    export standard_it_phase=$f/standard_it_phase
    export cooc=$f/corp.cooc
    export result_file=$OUTPUT_PATH$(basename $f)/$(ls $OUTPUT_PATH$(basename $f) | grep "AA3.final")

    echo $phase
    echo $standard_it
    echo $OUTPUT_PATH$(basename $f)
    echo $result_file

    ./plain2snt.out $phase $standard_it # convert the plain text to snt format
    ./snt2cooc.out $phase.vcb $standard_it.vcb $phase_standard_it.snt > $cooc # convert the snt format to cooc format
    ./GIZA++ -S $phase.vcb -T $standard_it.vcb -C $phase_standard_it.snt -CoocurrenceFile $cooc -outputpath $OUTPUT_PATH$(basename $f) # run giza++


    python ../giza-output-process.py $phase $standard_it $result_file > $OUTPUT_PATH$(basename $f)/alignment.out


done
