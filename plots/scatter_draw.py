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
import matplotlib.ticker as ticker

continent_month_files = "../../data/input/continent_month_split/"
scatter_figures_output = "../../data/output/plots/scatter_figures/"
bounds_file_path = "../../data/input/genome_list.tsv"

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

print("read data from genome_list.tsv")
data = pd.read_csv(bounds_file_path, sep="\t", header=None,names=['id', 'proteinName', 'gene', 'index'])
bounds = [1]
legend_labels = ["orf1a","orf1b"]
labels = ["5'UTR","orf1a","orf1b","NCR"]
for row_index, row in data.iterrows():
    if row["gene"] == "orf1ab":
        temp = row["index"].split(",")
        for item in temp:
            index_list = item.split("..")
            for index in index_list:
                if int(index) not in bounds:
                    bounds.append(int(index))
    else:
        legend_labels.append(row["gene"])
        labels.append(row["gene"])
        if row["gene"] == "ORF10":
            labels.append("3'UTR")
        else:
            labels.append("NCR")
        temp = row["index"].split("..")
        for item in temp:
            if int(item) not in bounds:
                bounds.append(int(item))
bounds.append(30000)
colors = ['white', '#63b2ee','#76da91','white','#f8cb7f','white','#f89588','white','#7cd6cf','white','#9192ab','white','#7898e1','white', '#efa666', 'white','#eddd86','white','#9987ce','white', '#63b2ee', 'white']
legend_colors = [c for c in colors if c != "white"]
print(bounds,len(bounds), labels, len(labels), len(legend_colors))

colors_dict = {
    0:colors[0:2],
    1:['#63b2ee'],
    2:['#63b2ee','#76da91'],
    3:['#76da91'],
    4:['#76da91','white','#f8cb7f'],
    5:['#f8cb7f','white','#f89588','white','#7cd6cf','white','#9192ab','white','#7898e1','white', '#efa666', 'white','#eddd86','white','#9987ce','white', '#63b2ee', 'white']
}

bounds_dict = {
    0:[1, 266, 5000],
    1:[5001, 10000],
    2:[10001, 13468, 15000],
    3:[15001, 20000],
    4:[20001, 21555, 21563, 25000],
    5:[25001, 25384, 25393, 26220, 26245, 26472, 26523, 27191, 27202, 27387, 27394, 27759, 27894, 28259, 28274, 29533, 29558, 29674, 30000]
}

labels_dict = {
    0:[1, 266, 5000],
    1:[5001, 10000],
    2:[10001, 13468, 15000],
    3:[15001, 20000],
    4:[20001, 21563, 25000],
    5:[25001, 25393, 26245, 26523, 27202, 27394, 27894, 28274, 29558, 30000]
}

legend_labels_dict = {
    0:["ORF1a"],
    1:["ORF1a"],
    2:["ORF1a","ORF1b"],
    3:["ORF1b"],
    4:["ORF1b", "S"],
    5:["S", "ORF3a","E", "M", "ORF6", "ORF7a", "ORF8", "N", "ORF10"]
}

print("reading data grouped by month and continent")
# 声明一个dict类型的空dict
continent_month_dict = defaultdict(lambda : {})
# 声明heatmap的横轴数组(29903bp)
genome_length = [i+1 for i in range(29903)]

splits = os.listdir(continent_month_files)
for split in tqdm(splits):
    print(split)
    # 获取文件名的大洲与月份
    continent, month = split.split(".")[0].split("-")
    month = month[0:4] + "-" + month[4:]
    # 读取文件数据
    data = pd.read_csv(continent_month_files + split, sep="\t")
    # # 将position的类型改为str
    # data["Position"] = data["Position"].astype(str)
    # 计算当月的样本数
    sample_num = len(data["Id"].unique())
    # 计算各个位点的出现个数并按照位点次序排序
    pos_series = data["Position"].value_counts().sort_index()
    # 判断是否存在position=0，如果有就删除该行
    keys = pos_series.keys()
    if 0 in keys:
        pos_series = pos_series.drop(0)
    # print(pos_series)
    pos_fre_series = pos_series / sample_num
    pos_indexs = list(pos_fre_series.keys())
    fre_res = []
    for i in genome_length:
        if i in pos_indexs:
            fre_res.append(round(pos_fre_series[i],2))
        else:
            fre_res.append(0)
    continent_month_dict[continent][month] = list(fre_res)

for continent in tqdm(continent_month_dict):
    print(continent)
    months = []
    heatmap_data = []
    sorted_continent_dict = sorted(continent_month_dict[continent].items(), key=lambda x: x[0]) 
    for month_data in sorted_continent_dict:
        print(month_data[0])
        month = month_data[0]
        months.append(month)
        heatmap_data.append(list(month_data[1]))
        print(len(month_data[1]))
        # months.append(month)
        # 进行热点图作图
    print("Start drawing")
    heatmap_data = np.array(heatmap_data)
    heatmap_data1 = np.array(heatmap_data[:,0:5000])
    heatmap_data2 = np.array(heatmap_data[:,5000:10000])
    heatmap_data3 = np.array(heatmap_data[:,10000:15000])
    heatmap_data4 = np.array(heatmap_data[:,15000:20000])
    heatmap_data5 = np.array(heatmap_data[:,20000:25000])
    heatmap_data6 = np.array(heatmap_data[:,25000:])

    heatmap_data_dict = {
    0:heatmap_data1,
    1:heatmap_data2,
    2:heatmap_data3,
    3:heatmap_data4,
    4:heatmap_data5,
    5:heatmap_data6,
}

    for i in range(6):
        plt.figure(figsize=(45,15))
        grid = plt.GridSpec(15, 45, hspace=0.8, right = 0.8)
        plt.subplot(grid[0:9,0:44])
        ax = sns.heatmap(heatmap_data_dict[i], cmap="PuRd", yticklabels=months, vmin=0,vmax=0.05, cbar=False)
        plt.xticks(ticks = [1,1000, 2000, 3000, 4000,5000],labels=[1+i*5000,1000+i*5000, 2000+i*5000, 3000+i*5000, 4000+i*5000,(1+i)*5000]) 
        ax.set_xticklabels(labels=[1+i*5000,1000+i*5000, 2000+i*5000, 3000+i*5000, 4000+i*5000,(1+i)*5000],fontsize=32, fontproperties=en_font)
        ax.set_yticklabels(labels=months, fontsize=32, fontproperties=en_font)
        ax.tick_params(top=True, bottom=False,
                       labeltop=True, labelbottom=False, labelsize=32)
        plt.setp(ax.get_xticklabels(), rotation=-0, ha="right",
                 rotation_mode="anchor")
        plt.setp(ax.get_yticklabels(), rotation=0, ha="right",
                 rotation_mode="anchor")
        ax = plt.subplot(grid[0:9, 44:])
        # cb=ax.figure.colorbar(ax.collections[0]) #显示colorbar
        # cb.ax.tick_params(labelsize=32) #设置colorbar刻度字体大小
        norm = mpl.colors.Normalize(vmin=0, vmax=0.05)
        cb = plt.colorbar(
            mpl.cm.ScalarMappable(norm=norm, cmap="PuRd"),
            cax=ax,
            ticks=[0,0.01, 0.02, 0.03, 0.04,0.05]
        )
        cb.ax.tick_params(labelsize=32)
        ax = plt.subplot(grid[9:10,0:44])
        cmap = mpl.colors.ListedColormap(colors_dict[i])
        norm = mpl.colors.BoundaryNorm(bounds_dict[i], cmap.N)
        cbar = plt.colorbar(
            mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
            cax=ax,
            ticks=[],
            spacing='proportional',
            orientation='horizontal',
        )
        # cbar.xticks(ticks=[(j-i*5000) for j in bounds_dict[i]],labels=[str(j) for j in bounds_dict[i]])
        # cbar.ax.tick_params(labelsize=32)
        # plt.setp(cbar.ax.get_xticklabels(), rotation=0, ha="right",
        #  rotation_mode="anchor")

        # cbar.ax.set_xticklabels([str(j) for j in bounds_dict[i]])
        cbar.outline.set_visible(False)
        # create a patch (proxy artist) for every color 
        label_colors = [c for c in colors_dict[i] if c != "white"]
        patches = [ mpatches.Patch(color=label_colors[j], label=legend_labels_dict[i][j]) for j in range(len(label_colors)) ]
        # put those patched as legend-handles into the legend
        # ax = plt.subplot(grid[10:,0:44])
        ncol = len(label_colors)
        lg = ax.legend(handles=patches, fontsize=32,bbox_to_anchor=(0.5,-3),loc=8,borderaxespad = 0.2,ncol=ncol, labelspacing=1 )


        plt.savefig(
        scatter_figures_output + "mutation_region-{}-{}.png".format(continent, i+1),bbox_extra_artists=(lg,),  bbox_inches="tight",dpi=500)
        plt.close()


    # plt.figure(figsize=(45,10))
    # grid = plt.GridSpec(10, 45, hspace=0.8, right = 0.8)
    # plt.subplot(grid[0:9,0:44])
    # ax = sns.heatmap(heatmap_data1, cmap="PuRd", yticklabels=months, vmin=0,vmax=0.05, cbar=False)
    # # plt.xticks(ticks = [1,2500, 5000, 7500, 10000],labels=[1,2500, 5000, 7500, 10000]) 
    # plt.xticks(ticks = [1,500, 1000, 1500, 2000,2500, 5000],labels=[1,500, 1000, 1500, 2000,2500, 5000]) 
    # ax.set_xticklabels(labels=[1,500, 1000, 1500, 2000,2500, 5000],fontsize=32, fontproperties=en_font)
    # ax.set_yticklabels(labels=months, fontsize=32, fontproperties=en_font)
    # ax.tick_params(top=True, bottom=False,
    #                labeltop=True, labelbottom=False, labelsize=32)
    # plt.setp(ax.get_xticklabels(), rotation=-0, ha="right",
    #          rotation_mode="anchor")
    # plt.setp(ax.get_yticklabels(), rotation=0, ha="right",
    #          rotation_mode="anchor")
    
    # ax = plt.subplot(grid[0:9, 44:])
    # # cb=ax.figure.colorbar(ax.collections[0]) #显示colorbar
    # # cb.ax.tick_params(labelsize=32) #设置colorbar刻度字体大小
    # norm = mpl.colors.Normalize(vmin=0, vmax=0.05)
    # cb = plt.colorbar(
    #     mpl.cm.ScalarMappable(norm=norm, cmap="PuRd"),
    #     cax=ax,
    #     ticks=[0,0.01, 0.02, 0.03, 0.04,0.05]
    # )
    # cb.ax.tick_params(labelsize=32)
    
    # ax = plt.subplot(grid[9,0:44])
    # cmap = mpl.colors.ListedColormap(colors_1)
    # norm = mpl.colors.BoundaryNorm(bounds_1, cmap.N)
    # cbar = plt.colorbar(
    #     mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
    #     cax=ax,
    #     ticks=[241, 266, 3037, 10000],
    #     spacing='proportional',
    #     orientation='horizontal',
    # )
    # cbar.outline.set_visible(False)
    # cbar.ax.tick_params(labelsize=32)

    # plt.savefig(
    #     scatter_figures_output + "mutation_region-{}-1.png".format(continent), bbox_inches="tight")
    # plt.close()



