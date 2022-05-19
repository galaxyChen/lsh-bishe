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

input_file_path = "../data/input/"
output_file_path = "../data/output/frequency_hap_csv/"
frequency_file_path = "../data/output/frequency_hap_csv/Europe/"
img_save_path = "../data/output/frequency_hap_csv/"

H12_fre = []
H12_month = []
H141_fre = []
H141_month = []

H12_pos = [241,445,3037, 6286, 14408, 21255, 22227, 23403, 26801, 28932, 29645]
H12_pos_fre = [[] for i in range(len(H12_pos))]
H141_pos = [241,913,3037,3267,5388,5986,6954, 11291,11296, 14408, 14676, 15279, 16176, 23063, 23271,23403,23604,23709, 24506, 24914, 27972, 28048, 28111, 28280,28281, 28282, 28881, 28882, 28883, 28977]
H141_pos_fre = [[] for i in range(len(H141_pos))]

def draw_hap(data, continent, month, num_sample, hap):
    temp = 0
    line = data[(data["hap"] == hap)]
    if len(line) > 0:
        temp = line["Frequency"].values[0]
    if hap == "H1-2":
        H12_fre.append(temp)
        H12_month.append(str(month))
    if hap == "H1-4-1":
        H141_fre.append(temp)
        H141_month.append(str(month))

def read_data(data, continent, month):
    num_sample = len(data["Id"].unique())
    hap_counts_16 = data["16sites"].value_counts(sort=False)
    haps_16 = hap_counts_16.index
    haps_fre_16 = hap_counts_16.values/num_sample

    hap_counts_30 = data["30sites"].value_counts(sort=False)
    haps_30 = hap_counts_30.index
    haps_fre_30 = hap_counts_30.values/num_sample

    res1 = pd.DataFrame()
    res1["hap"] = haps_16
    res1["Frequency"] = haps_fre_16
    res1["Frequency"] = res1["Frequency"].apply(lambda x: round(x, 4))
    draw_hap(res1, continent, month, num_sample, "H1-2")
    # res1.to_csv(output_file_path + "16/{}-{}-{}-{}.tsv".format(continent, "16sites", month, num_sample), index = False, sep = "\t")

    res2 = pd.DataFrame()
    res2["hap"] = haps_30
    res2["Frequency"] = haps_fre_30
    res2["Frequency"] = res2["Frequency"].apply(lambda x: round(x, 4))
    draw_hap(res2, continent, month, num_sample, "H1-4-1")
    # res2.to_csv(output_file_path + "30/{}-{}-{}-{}.tsv".format(continent, "30sites", month, num_sample), index = False, sep = "\t")

def read_snv_data(data, continent, month):
    for i, pos in enumerate(H12_pos):
        temp = 0
        line = data[(data["position"] == pos)]
        if len(line) > 0:
            temp = line["frequency"].values[0]
        H12_pos_fre[i].append(temp)
        # print(H12_pos_fre[i])
    for j, pos in enumerate(H141_pos):
        temp = 0
        line = data[(data["position"] == pos)]
        if len(line) > 0:
            temp = line["frequency"].values[0]
        H141_pos_fre[j].append(temp)


def draw_line(fre_data, month_data, num, hap):
    fre_data = fre_data[:num]
    month_data = month_data[:num]
    plt.plot(month_data, fre_data, markersize=5, label="frequency")
    #绘制坐标轴标签
    plt.xlabel("Month")
    plt.ylabel("Frequency")
    plt.title("{}-Frequency".format(hap))
    plt.xticks(rotation=-30)
    #显示图例
    plt.legend()
    for x1, y1 in zip(month_data, fre_data):
        plt.text(x1, y1, str(y1), ha='center', va='bottom', fontsize=10)
    #保存图片
    plt.savefig(img_save_path + "{}-Frequency.png".format(hap))
    plt.close()
    plt.clf()

def draw_pos_line(pos_data, fre_data,month_data, num, hap):
    fig = plt.figure(figsize=(60, 20))
    pos_data = pos_data[:num]
    month_data = month_data[:num]
    #绘制折线图，添加数据点，设置点的大小
    for y in fre_data:
        y = y[:num]
        plt.plot(month_data, y)
        # for a, b in zip(pos_data, y):
        #     plt.text(a, b, str(b), ha='center', va='bottom', fontsize=10)

    plt.title("{}-Position-Frequency".format(hap))  # 折线图标题
    plt.xlabel('Month')  # x轴标题
    plt.ylabel('Frequency')  # y轴标题
    plt.xticks(rotation=-30)
    #绘制图例
    plt.legend(pos_data, loc="best")
    plt.savefig(img_save_path + "{}-Position-Frequency".format(hap))
    plt.close()
    plt.clf()


print("reading data from H1-2 and H1-4-1")
H12_data = input_file_path + "kaks_info_Europe_filter.tsv"
data = pd.read_csv(H12_data, sep="\t")
for group, group_data in tqdm(data.groupby(["Month"])):
    read_data(group_data, "Europe", group)

print("reading data from snv")
splits = os.listdir(frequency_file_path)
for split in tqdm(splits):
    # split: continent-month.tsv
    group = split.split(".")[0]
    continent, month = group.split("-")[0], group.split("-")[1]
    group_data = pd.read_csv(frequency_file_path+split, sep="\t", names=["position", "frequency"])
    read_snv_data(group_data, continent, month)

print(len(H12_pos_fre[0]))
print(len(H141_pos_fre[0]))

draw_line(H12_fre, H12_month, 8, "H1-2")
draw_line(H141_fre, H141_month, 12, "H1-4-1")

draw_pos_line(H12_pos, H12_pos_fre,H12_month, 8, "H1-2")
draw_pos_line(H141_pos, H141_pos_fre, H141_month, 12, "H1-4-1")
