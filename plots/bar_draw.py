#-*- coding: utf-8 -*-
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

continent_month_dict = defaultdict(lambda : [])
continent_arr = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]

continent_month_input_path = "../../data/input/continent_month_split/"
bar_output_path = "../../data/output/plots/bar_figures/"

# 设置图表正常显示中文
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimSun']
# plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams["axes.unicode_minus"]=False
# plt.rcParams['text.usetex'] = True

print("reading data grouped by month and continent")
splits = os.listdir(continent_month_input_path)
for split in splits:
    # split: continent-month.tsv
    group = split.split(".")[0]
    continent, month = group.split("-")
    continent_month_dict[continent].append(split)

for continent in tqdm(continent_arr):
    file_arr = continent_month_dict[continent]
    month_fre_dict = defaultdict(lambda : {})
    print("Continent:", continent)
    # print(file_arr)
    for file in file_arr:
        group = file.split(".")[0]
        continent, month = group.split("-")
        data = pd.read_csv(continent_month_input_path + file, sep="\t")
        # 计算当月的样本数并保存进入dict
        sample_num = len(data["Id"].unique())
        month_fre_dict[month]["num"] = sample_num
        # print("month:", month)
        # print("num:", str(sample_num))
        # 计算位点的出现次数
        position_counts = data["Position"].value_counts()
        # 计算位点的频率series
        position_frequency = position_counts / sample_num
        # 分频率阶段统计个数
        # 0 - 0.01
        fre_1 = position_frequency[(position_frequency > 0) & (position_frequency < 0.01)]
        # print("0 - 0.01:", str(len(fre_1)))
        # 0.01 - 0.5
        fre_2 = position_frequency[(position_frequency >= 0.01) & (position_frequency < 0.05)]
        # print("0.01 - 0.05:", str(len(fre_2)))
        # 0.5 - 1.0
        fre_3 = position_frequency[(position_frequency >= 0.05) & (position_frequency <= 1)]
        # print("0.05 - 1.0:", str(len(fre_3)))
        # 将每个频率段的位点数输入当月的dict
        """
            0 —— 频率为 0-0.01
            0.05 —— 频率为 0.01-0.05
            1 —— 频率为 0.05-1
        """
        month_fre_dict[month]["0"] = len(fre_1)
        month_fre_dict[month]["0.05"] = len(fre_2)
        month_fre_dict[month]["1"] = len(fre_3)
    # 对month_fre_dict依照月份进行排序
    sorted_dict = sorted(month_fre_dict.items(), key=lambda x: x[0]) 
    # print(sorted_dict)
    # 获取堆叠柱状图需要的x坐标数组和y坐标数组
    """
        months —— x数组 每个大洲的月份
        y_1 —— 频率为0-0.01的所有位点百分比数据
        y_2 —— 频率为0.01-0.05的所有位点百分比数据
        y_3 —— 频率为0.05-1的所有位点百分比数据
        month_sample_num —— 每个月每个大洲包含突变位点位点个数
    """
    months = []
    y_1 = []
    y_2 = []
    y_3 = []
    month_sample_num = []
    sample_num = []
    for month_data in sorted_dict:
        # 更新月份格式为yyyy-mm
        month = month_data[0]
        new_month = month[0:4] + "-" + month[4:]
        months.append(new_month)
        # append样本数
        sample_num.append(month_data[1]["num"])
        # 每个月所有位点出现个数的总和
        pos_sum = sum([month_data[1]["0"], month_data[1]["0.05"], month_data[1]["1"]])
        # 将各个频率段的数据append进入y数组
        y_1.append(month_data[1]["0"] / pos_sum)
        y_2.append(month_data[1]["0.05"] / pos_sum)
        y_3.append(month_data[1]["1"] / pos_sum)
        # 记录各个月的位点突变个数总和
        month_sample_num.append(pos_sum)
    # 合并y数组为y_data二维数组，方便画堆叠柱状图
    y_data = [y_1, y_2, y_3]
    # 柱子颜色数组
    color_arr = ["#3D5488", "#00A086", "#E64B35"]
    # 初始化bottom_y数组
    bottom_y = [0 for i in range(len(months))]
    # 画堆叠柱状图
    plt.figure(figsize=(10,4))
    # 设置标题，x坐标和y坐标的标签，以及各个频率段的label
    # plt.title("{}在{}个月的位点突变频率分布柱状图".format(continent, len(months)), y=-0.12, fontsize=50)
    # plt.axhline(0.95, label="频率=0.95", color="red", linestyle ="--", lineWidth=1.75)
    data_label = [r"""$0<$突变频率$<1\%$""", r"""$1\%≤$突变频率$<5\%$""", r"""$5\%≤$突变频率$≤100\%$"""]
    for i, data in enumerate(y_data):
        plt.bar(months, data, bottom=bottom_y, width=0.7, label=data_label[i], color=color_arr[i])
        bottom_y = [(a+b) for a, b in zip(data, bottom_y)]
        # if i == 0:
        #     for x, y, z in zip(months, bottom_y, data):
        #         if z > 0:
        #             plt.text(x, y-0.04, '%.2f'%z, ha="center", fontsize=30)
    # for x, y, z in zip(months, bottom_y, month_sample_num):
    #     plt.text(x,y+0.01,z, ha='center', fontsize=18)
    # plt.xlabel("年月份（yyyy-mm）",fontsize=30, labelpad=8.5, loc="right")
    plt.ylabel("百分比（%）", fontsize=18, fontproperties=mix_font)
    plt.ylim(-0.05, 1.05)
    plt.xticks(fontsize=18, rotation=-45,horizontalalignment='left', fontproperties=en_font)
    plt.yticks([0,0.25,0.5,0.75,1],["0", "25", "50", "75", "100"],fontsize=18, fontproperties=en_font)
    plt.legend(loc=2, bbox_to_anchor=(1.01,1.0),borderaxespad = 0.,prop=mix_font)
    plt.savefig(bar_output_path + "bar-{}.png".format(continent), bbox_inches="tight", dpi=300)
    plt.close()

    print(months, sample_num)




        






