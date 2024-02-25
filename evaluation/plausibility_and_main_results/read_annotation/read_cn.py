import os


TOP_WORDS = 20

def read_tsv_exp1 (original_tsv_file):
    file = []
    # if the file is a xlsx file, convert it to tsv file
    # read the tsv file and store it into a list
    with open(original_tsv_file, 'r',encoding="utf-8") as f:
        # read the file line by line, the first line should start with "句子	算法 X	算法 Y..."
        for line in f:
            line = line.strip().split('\t')
            if len(line) != 1:
                file.append(line)

    return file[1:]

def read_tsv_exp2 (original_tsv_file):
    file = []
    # if the file is a xlsx file, convert it to tsv file
    # read the tsv file and store it into a list
    with open(original_tsv_file, 'r',encoding="utf-8") as f:
        # next(f)
        for line in f:
            if "EXAMPLE" in line:
                continue
            line = line.strip().split('\t')

            file.append(line)

    return file[1:]

def check_annotation (original_order, annotation_order, final_result):
    alg_x_count = 0
    alg_y_count = 0
    swap_count = 0

    for org, annot in zip(original_order, annotation_order):
        if "EXAMPLE" in org[0] or "EXAMPLE" in annot[0]:
            continue
        if org[0] != annot[0]:
            print("ERROR: The two sentences are different!")
            exit(1)
        else:
            if org[0] not in final_result:
                final_result[org[0]] = ""

        if org[1] == annot[1]:
            # means the original order is same as the annotation order, it was NOT swapped
            if annot[3].strip() == "x":
                alg_x_count += 1
                final_result[org[0]] += "x"
            elif annot[3].strip() == "y":
                alg_y_count += 1
                final_result[org[0]] += "y"
            elif annot[3].strip() == "b":
                # alg_x_count += 1
                # alg_y_count += 1
                # final_result[org[0]] += "x"
                # final_result[org[0]] += "y"
                final_result[org[0]] += "b"

                pass
            elif annot[3].strip() == "n":
                final_result[org[0]] += "n"
                pass
            else:
                print("ERROR: The annotation is wrong!")
                print(annot)
                exit(1)

        else:
            swap_count += 1
            # means the original order is different from the annotation order, it was swapped
            if annot[3].strip() == "x":
                alg_y_count += 1
                final_result[org[0]] += "y"

            elif annot[3].strip() == "y":
                alg_x_count += 1
                final_result[org[0]] += "x"

            elif annot[3].strip() == "b":
                # alg_x_count += 1
                # alg_y_count += 1
                # final_result[org[0]] += "y"
                # final_result[org[0]] += "x"
                final_result[org[0]] += "b"
                pass
            elif annot[3].strip() == "n":
                final_result[org[0]] += "n"
                pass
            else:
                print("ERROR: The annotation is wrong!")
                print(annot)
                exit(1)

    print("selfExp: ", alg_x_count)
    print("LOO: ", alg_y_count)
    #print("Swapped: ", swap_count)

def experiment_1 (original_tsv_file, annotator_folder):

    for experiment in ["1a", "1b"]:
        print(f"\n\n************ Experiment: [{experiment}] ************")

        original_order = read_tsv_exp1(original_tsv_file + f"{experiment}.tsv")

        # read the subfolder name
        annotators = [f.path for f in os.scandir(annotator_folder) if f.is_dir() ]

        final_result = {}

        for annotator in annotators:
            annotator_name = annotator.split("/")[-1]
            print("\nAnnotator: ", annotator_name)
            annotator_file = annotator + "/" + f"{experiment}.tsv"
            annotator_order = read_tsv_exp1(annotator_file)

            if len(original_order) != len(annotator_order):
                print("ERROR: The number of sentences in the two files are different!")
                exit(1)
            else:
                check_annotation(original_order, annotator_order,final_result)

        print(f"\n---------- Majority Voting ----------")
        result_count_x = 0
        result_count_y = 0
        result_count_both = 0
        result_count_none = 0


        for key in final_result:
            if "EXAMPLE" in key:
                continue

            result = final_result[key]
            # take out "b" and "n" from the result, for it
            # result = result.replace("b", "xy")
            # result = result.replace("n", "")

            # for cn
            #result = result.replace("b", "")

            # count the number of "x" and "y", and compare them to see which algorithm is better
            x_count = result.count("x")
            y_count = result.count("y")
            b_count = result.count("b")
            n_count = result.count("n")

            # find the max count and the variable name between x_count, y_count, b_count, and n_count
            max_count = max(x_count, y_count, b_count, n_count)
            max_name = ""
            if max_count == x_count:
                max_name = "x"
                result_count_x += 1
            elif max_count == y_count:
                max_name = "y"
                result_count_y += 1
            elif max_count == b_count:
                max_name = "b"
                result_count_both += 1
            elif max_count == n_count:
                max_name = "n"
                result_count_none += 1
            else:
                print("ERROR: The max count is wrong!")
                exit(1)

        print("Total number of sentences: ", len(final_result))
        print("Final count - selfExp: ", result_count_x)
        print("Final count - LOO: ", result_count_y)
        print("Final count - both: ", result_count_both)
        print("Final count - none: ", result_count_none)
        # print("Final score - selfExp: ", result_count_x/len(final_result))
        # print("Final score - LOO: ", result_count_y/len(final_result))


def experiment_2 (original_tsv_file, annotator_folder):

    # read the subfolder name
    orginal_files = [f.path for f in os.scandir(original_tsv_file) if f.is_file()]
    annotators = [f.path for f in os.scandir(annotator_folder) if f.is_dir()]

    for original_file in orginal_files:
        final_result = {}

        file_name = original_file.split("/")[-1].split(".")[0]
        experiment_name = ""

        if file_name == "loo":
            experiment_name = "Leave one out"
        elif file_name == "pr":
            experiment_name = "Pickup rate"
        elif file_name == "si":
            experiment_name = "Strong indicator"
        elif file_name == "st":
            experiment_name = "Combined Extraction method"

        print("\n\n************ Experiment: [", experiment_name, "] ************")

        current_original_words = read_tsv_exp2(original_file)[:TOP_WORDS]

        left_words = []
        right_words = []

        for line in current_original_words:
            if line != "":
                if len(line) == 2:
                    left_words.append(line[0])
                    right_words.append(line[1])
                elif len(line) == 1:
                    left_words.append(line[0])
                    # right_words.append("")

        total_x_count_left = 0
        total_y_count_left = 0
        total_both_count_left = 0
        total_none_count_left = 0

        total_x_count_right = 0
        total_y_count_right = 0
        total_both_count_right = 0
        total_none_count_right = 0

        for annotator in annotators:
            annotator_name = annotator.split("\\")[-1]
            print("\nAnnotator: ", annotator_name)
            annotator_file = annotator + "/2.tsv"
            annotator_words = read_tsv_exp2(annotator_file)[1:]

            cleaned_annotator_words = []
            for line in annotator_words:
                if len(line) != 1 and "EXAMPLE" not in line[0]:
                    cleaned_annotator_words.append(line)
                # if len(line) ==1:
                #     print(line)

            correct_left_words = []
            correct_right_words = []

            x_count_tmp_left = 0
            y_count_tmp_left = 0
            both_count_tmp_left = 0
            none_count_tmp_left = 0

            x_count_tmp_right = 0
            y_count_tmp_right = 0
            both_count_tmp_right = 0
            none_count_tmp_right = 0

            # if left and TW words are appeared in cleaned_annotator_words,
            # when the "*" is in the first element, it means the left word is correct
            # when the "*" is in the second element, it means the right word is correct
            for line in cleaned_annotator_words:
                current_word = line[0]
                mark = ""
                if len(line) == 2:
                    mark = "x" # left
                elif len(line) == 3:
                    mark = "y" # right
                elif len(line) == 4:
                    mark = "b" # both
                elif len(line) == 5:
                    mark = "n" # none
                elif len(line) == 6:
                    mark = "u" # unknown

                if current_word in final_result:
                    final_result[current_word] += mark
                else:
                    final_result[current_word] = mark

                if current_word in left_words:
                    # if current_word not in right_words:
                    if len(line) == 2:
                        x_count_tmp_left += 1
                    elif len(line) == 3:
                        y_count_tmp_left += 1
                    elif len(line) == 4:
                        both_count_tmp_left += 1
                    elif len(line) == 5:
                        none_count_tmp_left += 1

                if current_word in right_words:
                    # if current_word not in left_words:
                    if len(line) == 2:
                        x_count_tmp_right += 1
                    elif len(line) == 3:
                        y_count_tmp_right += 1
                    elif len(line) == 4:
                        both_count_tmp_right += 1
                    elif len(line) == 5:
                        none_count_tmp_right += 1

            # total_x_count_left += x_count_tmp_left
            # total_y_count_left += y_count_tmp_left
            # total_both_count_left += both_count_tmp_left
            # total_none_count_left += none_count_tmp_left
            #
            # total_x_count_right += x_count_tmp_right
            # total_y_count_right += y_count_tmp_right
            # total_both_count_right += both_count_tmp_right
            # total_none_count_right += none_count_tmp_right

            print("\nx, CN words:")
            print(f"Number of x: {x_count_tmp_left}")
            print(f"Number of y: {y_count_tmp_left}")
            print(f"Number of both: {both_count_tmp_left}")
            print(f"Number of none: {none_count_tmp_left}")
            print("--------------------")
            print("y, TW words:")
            print(f"Number of x: {x_count_tmp_right}")
            print(f"Number of y: {y_count_tmp_right}")
            print(f"Number of both: {both_count_tmp_right}")
            print(f"Number of none: {none_count_tmp_right}")
            print("--------------------")
            # print(f"Total number of words in x: {len(left_words)}")
            # print(f"Total number of words in y: {len(right_words)}")
            # print("--------------------")

            # print("\n---------- Majority Voting per annotations----------")
            # print(f"Number of x: {x_count_tmp_left}")
            # print(f"Number of y: {y_count_tmp_left}")
            # print(f"Number of both: {both_count_tmp_left}")
            # print(f"Number of none: {none_count_tmp_left}")

            # print(f"Number of CN words: {len(correct_left_words)} out of {len(left_words)}")
            # print(f"Number of TW words: {len(correct_right_words)} out of {len(right_words)}")
            # print(f"Score in CN: {len(correct_left_words)/len(left_words)}")
            # print(f"Score in TW: {len(correct_right_words)/len(right_words)}")

        # if it is zh file:
        if "cn-tw" in original_file:
            print("********* Majority Voting *********")

            for pair in final_result:
                # perform majority voting
                result = final_result[pair]
                # take out "b" and "n" from the result, for it
                # result = result.replace("b", "xy")
                # result = result.replace("n", "")

                # for cn
                #result = result.replace("b", "")

                # count the number of "x" and "y", and compare them to see which algorithm is better
                x_count = result.count("x")
                y_count = result.count("y")
                b_count = result.count("b")
                n_count = result.count("n")

                max_count = max(x_count, y_count, b_count, n_count)
                max_name = ""
                if max_count == x_count:
                    max_name = "x"
                elif max_count == y_count:
                    max_name = "y"
                elif max_count == b_count:
                    max_name = "b"
                elif max_count == n_count:
                    max_name = "n"
                else:
                    print("ERROR: The max count is wrong!")
                    exit(1)
                final_result[pair] = max_name

                # if x_count > y_count:
                #     final_result[pair] = "x"
                # elif x_count < y_count:
                #     final_result[pair] = "y"
                # elif x_count == y_count:
                #     final_result[pair] = "xy"
                # else:
                #     if "建立" in pair or "其他" in pair:
                #         final_result[pair] = "x" # "其他" and "建立" are both "x" in CN dataset
                #     else:
                #         print("\nERROR: The number of x and y are the same!")
                #         print("Pair: ", pair)

            final_left_words = []
            final_right_words = []
            final_both_words = []
            final_none_words = []

            for pair in final_result:
                current_word = pair
                if current_word in left_words:
                    if final_result[pair] == "x":
                        final_left_words.append(current_word)
                    elif final_result[pair] == "b":
                        final_both_words.append(current_word)
                    elif final_result[pair] == "n":
                        final_none_words.append(current_word)
                if current_word in right_words:
                    if final_result[pair] == "y":
                        final_right_words.append(current_word)
                    elif final_result[pair] == "b":
                        final_both_words.append(current_word)
                    elif final_result[pair] == "n":
                        final_none_words.append(current_word)

            print(f"Number of CN words: {len(final_left_words)} out of {len(left_words)}")
            print(f"Number of TW words: {len(final_right_words)} out of {len(right_words)}")

            # print(f"Score in CN: {len(final_left_words)/len(left_words)}")
            # print(f"Score in TW: {len(final_right_words)/len(right_words)}")

            print(f"Number of both words: {len(final_both_words)}")
            print(f"Number of none words: {len(final_none_words)}")



        if file_name == "st":
            # lang_pair is two folder before annotator_folder
            lang_pair = annotator_folder.split("/")[-3]
            current_exp = annotator_folder.split("/")[-2]
            # st_folder is the same folder as the one in current python file
            st_folder = os.path.dirname(os.path.realpath(__file__)) + f"/{lang_pair}/{current_exp}/st_break_down_exp_2"

            if not os.path.exists(st_folder):
                print("\nERROR: st_break_down_exp_2 folder does not exist!")
                exit(1)
            for cur_class in ["class_0", "class_1"]:
                print(f"\n\n------------ Salient Token Break Down for Class: {cur_class.split('_')[1]} ------------")

                for tsv_file in ["agg.tsv","freq.tsv","tfidf.tsv"]:
                    correct_words = []

                    current_file = st_folder + "/" + cur_class + "/" + tsv_file
                    if not os.path.exists(current_file):
                        print(f"ERROR: {current_file} does not exist!")
                        exit(1)

                    current_words = read_tsv_exp2(current_file)
                    # only keep the first element in each line
                    current_words = [line[0] for line in current_words][:TOP_WORDS]

                    for pair in final_result:
                        current_word = pair

                        if current_word in current_words:
                            if final_result[pair] == "x" and cur_class == "class_0":
                                correct_words.append(current_word)
                            elif final_result[pair] == "y" and cur_class == "class_1":
                                correct_words.append(current_word)
                            elif final_result[pair] == "xy":
                                correct_words.append(current_word)

                    print(f"Number of correct words in [{tsv_file.split('.')[0]}]: {len(correct_words)} out of {len(current_words)}")
                    print(f"Score in [{tsv_file.split('.')[0]}]: {len(correct_words)/len(current_words)}\n")


def main ():

    #root_folder = "it-scn/selfExp-evaluation"
    #root_folder = "it-scn/loo-evaluation"
    root_folder = "cn-tw/loo-evaluation"
    #root_folder = "cn-tw/selfExp-evaluation"

    original_folder = root_folder + "/original_orders"
    annotator_folder = root_folder + "/annotators"

    #experiment_1(original_folder + "/exp_1/", annotator_folder)

    experiment_2(original_folder + "/exp_2/", annotator_folder)


if __name__ == '__main__':
    main ()
