from calendar import c
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as mpatches
from tqdm import tqdm
import matplotlib as mpl
import os
import seaborn as sns
from collections import defaultdict
from matplotlib.font_manager import FontProperties
def get_mix_font():
    font = FontProperties()
    font.set_family('sans-serif')
    font.set_name('Simsun')
    font.set_size("x-large")
    font.set_math_fontfamily('stix')
    return font

def get_en_font():
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    return font

mix_font = get_mix_font()
en_font=get_en_font()

continent_month_input_path = "../../data/input/continent_month_split/"
figures_output_path = "../../data/output/plots/mutation_type_figures/"

def get_bp_change(data):
    bp_change = str(data["Ref"]) + ">" + str(data["Alt"])
    return bp_change

continent_change_dict = defaultdict(lambda : {})

print("reading data grouped by month and continent")
splits = os.listdir(continent_month_input_path)
for split in splits:
    # split: continent-month.tsv
    group = split.split(".")[0]
    continent, month = group.split("-")
    month = month[0:4] + "-" + month[4:]
    print(continent, month)
    keys = continent_change_dict[continent].keys()
    data = pd.read_csv(continent_month_input_path + split, sep="\t")
    data["bp_change"] = data.apply(get_bp_change,axis=1)
    change_series = data["bp_change"].value_counts(normalize=True)
    change_indexs = np.array(change_series.keys())
    # print(change_indexs)
    if "0<0" in change_indexs:
        change_series = change_series.drop("0<0") 
    temp_dict = {}
    for i in change_indexs:
        if i in keys:
            continent_change_dict[continent][i].append(change_series[i])
        else:
            continent_change_dict[continent][i] = [change_series[i]]
    print(continent_change_dict[continent])
    # print(change_series)

for continent in continent_change_dict:
    labels = []
    data = []
    print(continent)
    for i in continent_change_dict[continent]:
        print(i)
        if str(i) != "nan>nan":
            labels.append(str(i))
            data.append(continent_change_dict[continent][i])
    print(labels)
    plt.figure()
    plt.boxplot(data, labels=labels, vert=True)
    plt.savefig(figures_output_path + "box-{}.png".format(continent), bbox_inches="tight", dpi=300)
    plt.close()
