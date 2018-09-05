"""Script used to generate confusion matrix graph """
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt


def generate_graph(
        classes,
        array,
        title='Confusion matrix',
        output='confusion_matrix.png'):
    """Method used to generate graph
    Args:
        classes: dataset classes
        array: matrix of values
        title: Title image
        output: output filename
    Returns:
        Write a file with output filename
    """
    norm = []
    for i in array:
        a_val = 0
        tmp_arr = []
        a_val = sum(i, 0)
        for j in i:
            tmp_arr.append((float(j)/float(a_val))*100)
        norm.append(tmp_arr)
    df_cm = pd.DataFrame(
        norm,
        index=[i for i in classes],
        columns=[i for i in classes])
    fig = plt.figure(figsize=(9, 9))
    fig.suptitle(title, fontsize=20)
    sn.heatmap(df_cm, annot=True)
    plt.savefig(output, format='png')


if __name__ == '__main__':
    # CLASSES = [
    #     'corynespora',
    #     'tetranychus',
    #     'tomato yellow',
    #     'healthy',
    #     'alternaria',
    #     'septoria',
    #     'xanthomonas',
    #     'phytophthora']
    CLASSES = [
        'tetranychus',
        'noise',
        'healthy',
        'alternaria',
        'xanthomonas']
    ARRAY = [[7543, 23, 289, 45, 14],
                [57, 7101, 383, 402, 142],
                [434, 320, 6184, 556, 542],
                [93, 334, 654, 6220, 743],
                [24, 89, 695, 869, 6344]]
    # ARRAY = [[7726,   13,  276,   18,   29],
    #       [71, 7180,  307,  294,  136],
    #       [655,  351, 6152,  438,  423],
    #       [159,  221,  467, 6496,  671],
    #       [59,   74,  647,  861, 6386]]
#     ARRAY = [[8771,  528,  457,  224],
#  [ 539, 8330,  580,  525],
#  [ 313,  736, 8232,  767],
#  [  95,  751,  992, 8260]]
    # ARRAY = [[11707,   975,   788],
    #     [  898, 11633,   838],
    #     [ 1285,   663, 11313]]
    #     ARRAY = [[827,  51,   9,  27,   6,  22,  50,   3],
#  [ 56, 903,  10,  28,   0,  12,   6,   0],
#  [  1,  43, 905,   2,   0,  33,  46,   0],
#  [ 74,  39,   0, 905,   0,  19,   0,   0],
#  [ 30,  15,   0,   6, 766,  45,  43,  61],
#  [ 70,   7,   0,  17,  44, 847,  40,   7],
#  [ 41,   6,   3,   0,  17,  34, 918,   1],
#     ARRAY = [[4328,  276,    8,  153,   40,  159,    5,   19],
#  [  48, 4919,    0,   24,    0,   21,    0,    0],
#  [   2,   73, 4868,    7,    0,    9,   60,    0],
#  [ 175,   79,    0, 4692,    2,    8,    0,    0],
#  [ 158,   18,    1,   49, 4510,  201,  105,   45],
#  [ 117,    4,    2,   15,   30, 4825,    9,    5],
#  [  12,    3,   26,   10,   18,   41, 4961,    0],
#  [ 111,    7,    0,   18,   53,  108,    4, 4659]]
#     ARRAY = [[4530,  130,   33,  141,   82,   50,   29,   40],
#  [ 123, 4828,   11,   21,    2,   13,    7,    4],
#  [   3,   28, 4858,    0,    0,    2,  105,    0],
#  [ 222,   90,    0, 4704,    3,    8,    1,    5],
#  [ 113,    3,    0,   68, 4528,   86,  118,   75],
#  [ 127,    2,    1,    0,   96, 4737,   14,   20],
#  [   4,    2,   17,    0,   13,   32, 4919,    0],
#  [  52,    3,    1,    2,  100,   76,    0, 4818]]
#  [ 37,   3,   0,  13,  43,  25,   3, 881]]
    # ARRAY = [[3931, 577, 45, 103, 15, 118, 250, 26],
    #          [146, 4637, 60, 53, 0, 50, 30, 6],
    #          [19, 170, 4607, 6, 0, 84, 183, 0],
    #          [401, 197, 0, 4417, 0, 0, 0, 0],
    #          [172, 131, 19, 75, 3757, 239, 258, 274],
    #          [226, 29, 2, 77, 156, 4241, 249, 14],
    #          [226, 43, 47, 3, 27, 96, 4643, 3],
    #          [287, 44, 2, 75, 180, 107, 2, 4265]]
    TITLE = 'Confusion matrix alternaria, xanthomonas and tetranychus - MobileNet v1.0 128'
    generate_graph(CLASSES, ARRAY, TITLE,
                   'confusion_matrix_alternaria_xanthomonas_tetranychus_mobilenet.png')
