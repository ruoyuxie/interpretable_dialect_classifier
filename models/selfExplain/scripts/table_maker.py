import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

def draw_bar_graph():
    # Define the data for y-axis (adequate justification percentages)

 

    # Use Seaborn styles
    sns.set()

    # assuming these are your word-count dictionaries
    explanation_word_counts = {
        '菠萝': 5,
        '鼠标': 7,
        '创可贴': 2,
        '博客': 4,
        '新西兰': 6,
        '打印机': 3,
        '站台': 8,
        '过山车': 1,
        '三文鱼': 9,
        '洗发水': 2,
        '软件': 3,
        '悉尼': 3,
        '回形针': 3
    }

    input_text_word_counts = {
        '菠萝': 5,
        '鼠标': 7,
        '创可贴': 2,
        '博客': 4,
        '新西兰': 6,
        '打印机': 3,
        '站台': 8,
        '过山车': 1,
        '三文鱼': 9,
        '洗发水': 2,
        '软件': 3,
        '悉尼': 3,
        '回形针': 3
    }
    # Create two lists of counts, in the order of 'all_words'
    all_words = list(set(explanation_word_counts.keys()).union(set(input_text_word_counts.keys())))
    explanation_counts = [explanation_word_counts.get(word, 0) for word in all_words]
    input_text_counts = [input_text_word_counts.get(word, 0) for word in all_words]

    # setup the plot
    x = list(range(len(all_words)))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar([i - width/2 for i in x], explanation_counts, width, label='Explanation')
    rects2 = ax.bar([i + width/2 for i in x], input_text_counts, width, label='Input Text')

    # Add some text for labels, and custom x-axis tick labels, etc.
    ax.set_ylabel('Counts')
    ax.legend()

    # set y-axis limit
    ax.set_ylim([0, 15])

    # Remove the grid
    ax.grid(False)

    # Add counts on top of the two bar graphs
    for rect in rects1 + rects2:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.0 * height,
                '%d' % int(height), ha='center', va='bottom')

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.25)  # create more space for the title and x-axis labels at the bottom

    # specify the font and apply it to the labels
    font_path = '/usr/share/fonts/thai-scalable/Waree-Bold.ttf'  # specify the actual font file path here
    prop = fm.FontProperties(fname=font_path)

    for label in ax.get_xticklabels():
        label.set_fontproperties(prop)
    ax.set_title('Word counts in explanation vs input text', fontproperties=prop)

    
    # Save the plot as an image
    plt.savefig('bar_graph.png')

# Call the function to draw the bar graph and save it
draw_bar_graph()
