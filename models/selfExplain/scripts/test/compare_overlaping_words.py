import sys

def main():
    exp_file = open("/scratch/rxie/selfexplain/my-self-exp/scripts/test/csv", "r", encoding="utf-8")
    train_file = open("/scratch/rxie/selfexplain/my-self-exp/scripts/test/tsv", "r", encoding="utf-8")
   
    # read each file line by line into a list
    exp_lines = exp_file.readlines()
    train_lines = train_file.readlines()
    exp_file.close()
    train_file.close()

    # check the length of the two lists
    if len(exp_lines) != len(train_lines):
        print("The two files have different number of lines!")
        sys.exit()

    exp_lists = []
    train_lists = []
    # break the lists into sublists baseed on the "\n"
    same_words = []

    for line_num in range(len(exp_lines)):
        current_line = exp_lines[line_num]
        if current_line.__contains__("tokens by"):
            continue
        else:
            exp_lists.append(current_line)
            train_lists.append(train_lines[line_num])

    for word in exp_lists:
        if word in train_lists:
            same_words.append(word)

    print("\n")
    print("Comparsion has [", len(same_words), "] words or [", len(same_words)/len(exp_lists), "] percentage of words are the same")
    print("*"   * 20)
    print("\n")


 
if __name__ == "__main__":
    main()