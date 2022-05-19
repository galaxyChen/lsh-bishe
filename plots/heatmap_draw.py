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
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# font = FontProperties()
# SimSun = FontProperties(fname="/home/lsh/anaconda3/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimSun.ttf")
# Times = FontProperties(fname="/home/lsh/anaconda3/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/TimesNewRoman.ttf")

# config = {
#     "font.family":'serif',
# #     "font.size": 80,
#     "font.style":"normal",
#     "mathtext.fontset":'stix',
#     "font.serif": "Times New Roman",
# }
# rcParams.update(config)
def get_en_font():
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    return font

en_font = get_en_font()

# 设置图表正常显示中文
plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams["font.style"] = "normal"
plt.rcParams["axes.unicode_minus"]=False

input_files_path = "../../data/input/World_data/"
output_files_path = "../../data/output/plots/heatmap_figures/"

print("Reading data grouped by months")
splits = os.listdir(input_files_path)
for split in tqdm(splits):
    # 保存每个文件的月份，修改格式为yyyy-mm
    month = split.split(".")[0]
    month = month[0:4] + "-" + month[4:]
    print("Month:", month)
    # 创建空的dict
    continent_pos_fre_dict = {}
    # 读取文件
    data = pd.read_csv(input_files_path + split, sep="\t")
    # 按照各个大洲进行分组
    for continent, group_data in data.groupby("Continent"):
        # 大洲在当月的样本量
        sample_num = len(group_data["Id"].unique())
        # print("Continent:", continent, "and samples:", str(sample_num))
        # 计算每个大洲每个月的SNV数量及频率
        snv_counts = group_data["SNV"].value_counts()
        snv_fres = snv_counts / sample_num
        # 筛选突变频率大于等于0.01的所有SNV位点并存入dict中
        filter_snv_fres = snv_fres[snv_fres >= 0.01]
        continent_pos_fre_dict[continent] = filter_snv_fres
    # 将dict中的key提取出来做为大洲list
    continents = list(continent_pos_fre_dict.keys())
    # 利用两重遍历dict并对数据进行公式计算，得出相似性
    """
        x —— 大洲1
        y —— 大洲2
        heatmap_data —— 用于画图的二维数组数据
    """
    heatmap_data = []
    for x in continents:
        # 保存一个大洲对其他大洲的相似性数据
        temp_arr = []
        for y in continents:
            # 获取两个大洲的series分别为x和y
            x_fre_series = continent_pos_fre_dict[x]
            y_fre_series = continent_pos_fre_dict[y]
            # 获取两个大洲的SNV及其频率的list
            x_fre_index = list(x_fre_series.index)
            y_fre_index = list(y_fre_series.index)
            # 统计两个大洲相同的突变位点
            common_mutations = list(set(x_fre_index).intersection(set(y_fre_index)))
            # 共同突变位点频率为common_fre
            common_fre = 0
            for mutation in common_mutations:
                common_fre += (x_fre_series[mutation] + y_fre_series[mutation]) / 2
            # 不同的突变位点频率为diff_fre
            diff_fre = 0
            # 分别对两个大洲的不同突变位点进行统计
            x_diff_mutations = list(set(x_fre_index).difference(set(y_fre_index)))
            y_diff_mutations = list(set(y_fre_index).difference(set(x_fre_index)))
            for mutation in x_diff_mutations:
                diff_fre += x_fre_series[mutation]
            for mutation in y_diff_mutations:
                diff_fre += y_fre_series[mutation]
            # 计算相似性
            fre = common_fre / (common_fre + diff_fre)
            temp_arr.append(fre)
        # 将temp_arr插入heatmap_data
        heatmap_data.append(temp_arr)
    # 进行热点图作图
    ax = sns.heatmap(heatmap_data, cmap="RdBu_r", xticklabels=continents,yticklabels=continents, annot_kws={'size':12}, linewidths=0.3, annot=True,vmin=0,vmax=1,fmt=".2f", cbar=False)
    ax.set_xticklabels(labels=continents, fontsize=16, fontproperties=en_font)
    ax.set_yticklabels(labels=continents, fontsize=16, fontproperties=en_font)
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False, labelsize=16)
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), rotation=0, ha="right",
             rotation_mode="anchor")
    
    cb=ax.figure.colorbar(ax.collections[0]) #显示colorbar
    cb.ax.tick_params(labelsize=16) #设置colorbar刻度字体大小
    
    plt.savefig(
        output_files_path + "heatmap-{}.png".format(month), bbox_inches="tight")
    plt.close()



        



