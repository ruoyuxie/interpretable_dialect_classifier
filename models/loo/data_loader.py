import json

def get_idti_lexicon(lexicon_silver_path):
    # get the base path of the json file, which is last and second last folder
    # if "all" in json_file_path:
    #     base_path = os.path.dirname(os.path.dirname(os.path.dirname(json_file_path)))
    # else:
    #     base_path = os.path.dirname(os.path.dirname(json_file_path))
    # lexicon_silver_path = os.path.join(base_path, "lexicon_silver")

    lexicon = {}
    reversed_lexicon = {}
    # read the lexicon_silver file
    with open(lexicon_silver_path, 'r', encoding="utf-8") as input_file:
        lexicon_silver = input_file.readlines()
        # split the lines into italian and dialect words by " - "
        lexicon_silver = [line.split(" - ") for line in lexicon_silver]
        for line in lexicon_silver:
            # remove the newline character
            line[1] = line[1].replace("\n", "").lower()
            line[0] = line[0].lower()
            # make sure the key and value only appear once
            if line[0] not in lexicon and line[1] not in reversed_lexicon:
                if line[0] != line[1]:
                    lexicon[line[1]] = line[0]
                    reversed_lexicon[line[0]] = line[1]

    return lexicon

def get_test_data(test_path):
    with open(test_path, 'r', encoding="utf-8") as input_file:
        data = []
        for k, line in enumerate(input_file):
            json_line = json.loads(line)
            sentence = json_line["sentence"]
            label = json_line["label"]
            data.append((sentence, label))
    # only keep first 50 sentences
    #data = data[:10]
    return data

def get_train_data(json_file,lang_flag,lexicon_silver_path):
    with open(json_file, 'r', encoding="utf-8") as input_file:
        data = []
        if lang_flag =="cn-tw":
            lexicon, _ = get_frmt_lexicon()
        if lang_flag =="it":
            lexicon = get_idti_lexicon(lexicon_silver_path)

        for k, line in enumerate(input_file):
            json_line = json.loads(line)
            sentence = json_line["sentence"]
            label = json_line["label"]
            data.append((sentence, label))

    # only keep first 50 sentences
    #data = data[:50]
    return data

def get_frmt_lexicon():
    # Format: English: (Simp-CN, Simp-TW, Trad-TW, Trad-CN)
    orginal_zh_terms = {
        "Pineapple": ("菠萝", "凤梨", "鳳梨", "菠蘿"),
        "Computer mouse": ("鼠标", "滑鼠", "滑鼠", "鼠標"),
        # Original source had CN:牛油果, but translator used 鳄梨.
        # "Avocado": ("鳄梨", "酪梨", "酪梨", "鱷梨"),
        "Band-Aid": ("创可贴", "OK绷", "OK繃", "創可貼"),
        "Blog": ("博客", "部落格", "部落格", "博客"),
        "New Zealand": ("新西兰", "纽西兰", "紐西蘭", "新西蘭"),
        "Printer (computing)": ("打印机", "印表机", "印表機", "打印機"),
        # Original source has TW:月臺, but translator used 月台.
        "Railway platform": ("站台", "月台", "月台", "站台"),
        "Roller coaster": ("过山车", "云霄飞车", "雲霄飛車", "過山車"),
        "Salmon": ("三文鱼", "鲑鱼", "鮭魚", "三文魚"),
        "Shampoo": ("洗发水", "洗发精", "洗髮精", "洗髮水"),
        # From Wikipedia page "Software testing"
        "Software": ("软件", "软体", "軟體", "軟件"),
        "Sydney": ("悉尼", "雪梨", "雪梨", "悉尼"),
        "test1": ("测试1", "测试2", "测试11", "测试4"),
        "test2": ("测试2", "测试6", "测试22", "测试8"),

        # The following two are excluded because they underpin the first 100
        # lexical exemplars used for priming the models.
        # "Flip-flops": ("人字拖", "夹脚拖", "夾腳拖", "人字拖"),
        "Paper clip": ("回形针", "回纹针", "迴紋針", "回形針")
    }

    # Portuguese terms.
    # Format: English: (BR, PT)
    # The Portuguese corpus is lowercased before matching these terms.
    orginal_pt_terms = {
        # "Bathroom": ("banheiro", "casa de banho"),
        # Original source had "pequeno almoço" but translator used "pequeno-almoço".
        # "Breakfast": ("café da manhã", "pequeno-almoço"),
        "Bus": ("ônibus", "autocarro"),
        "Cup": ("xícara", "chávena"),
        "Computer mouse": ("mouse", "rato"),
        # "Drivers license": ("carteira de motorista", "carta de condução"),
        # From Wikipedia page "Ice cream sandwich"
        "Ice cream": ("sorvete", "gelado"),
        "Juice": ("suco", "sumo"),
        "Mobile phone": ("celular", "telemóvel"),
        "Pedestrian": ("pedestre", "peão"),
        # From Wikipedia page "Pickpocketing"
        # "Pickpocket": ("batedor de carteiras", "carteirista"),
        "Pineapple": ("abacaxi", "ananás"),
        "Refrigerator": ("geladeira", "frigorífico"),
        "Suit": ("terno", "fato"),
        "Train": ("trem", "comboio"),
        "Video game": ("videogame", "videojogos"),

        # Terms updated after original selection.

        # For BR, replaced "menina" (common in speech) with "garota" (common in
        # writing, matching the human translators.
        "Girl": ("garota", "rapariga"),

        # Replace original "Computer monitor": ("tela de computador", "ecrã") with
        # the observed use for just screen:
        "Screen": ("tela", "ecrã"),

        # Terms excluded.

        # The following three are excluded because they underpin the first 100
        # lexical exemplars used for priming the models.
        "Gym": ("academia", "ginásio"),
        "Stapler": ("grampeador", "agrafador"),
        # "Nightgown": ("camisola", "camisa de noite"),

        # The following are excluded for other reasons:

        # BR translator primarily used 'comissário de bordo' and hardly ever
        # 'aeromoça'. PT translator used 'comissários/assistentes de bordo' or just
        # 'assistentes de bordo' Excluding the term as low-signal for now.
        ## "Flight attendant": ("aeromoça", "comissário ao bordo"),

        # Both regions' translators consistently used "presunto", so the term has
        # low signal.
        ## "Ham": ("presunto", "fiambre"),
    }

    zh_lexicon = {}
    pt_lexicon = {}

    # for each language, create a dictionary of terms
    for orginal_terms in [orginal_zh_terms, orginal_pt_terms]:
        for term, translations in orginal_terms.items():
            # if it's chinese
            if len(translations) == 4:
                # only care about Simp-CN and Trad-TW
                zh_lexicon[translations[0]] = translations[2]
            else:
                # only care about BR and PT
                pt_lexicon[translations[0]] = translations[1]

    return zh_lexicon, pt_lexicon