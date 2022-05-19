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

filter_file_path = "../data/input/snp_merged_adjusted_filter.tsv"
bounds_file_path = "../data/input/genome_list.tsv"
scatter_save_path = "../data/output/scatter_figures/"
hist_save_path = "../data/output/hist_figures/"
csv_save_path = "../data/output/heatmap_position_csv/"

def heatmap_draw(grid, grid_index, begin_fre, end_fre, old_heatmap_positions, old_heatmap_counts, continent, month, num_sample):
    heatmap_counts = []
    heatmap_positions = []
    for i in range(len(old_heatmap_counts)):
        if begin_fre<=old_heatmap_counts[i]<end_fre:
            heatmap_positions.append(old_heatmap_positions[i])
            heatmap_counts.append(old_heatmap_counts[i])
    heatmap_res = []
    res = []
    left_index = 1
    right_index = 100
    for index in range(300):
        temp = 0
        position = ""
        range_str = str(left_index) + ".." + str(right_index)
        for i, pos in enumerate(heatmap_positions):
            if pos >= left_index and pos <= right_index:
                gene = ""
                for j in range(len(bounds)-1):
                    left, right = bounds[j], bounds[j+1]
                    if left<=pos<=right:
                        gene = labels[j]
                        break
                position += (str(pos) + "-" + str(format(heatmap_counts[i],'.4f')) + "-" + gene +  ",")
                temp += 1
        if temp > 0:
            res.append({
                "Range":range_str,
                "Count":int(temp),
                "Position":position
            })
        heatmap_res.append(temp)
        left_index += 100
        right_index += 100
    if len(res) > 0:
        res = pd.DataFrame(res)
        res.to_csv(csv_save_path + str(grid_index-14) + "/heatmap-{}-{}-{}-{}-output.tsv".format(continent, month, num_sample, grid_index-14), index=False, header=True, sep="\t")
    if grid_index < 20:
        plt.subplot(grid[grid_index,0])
        plt.imshow([heatmap_res], cmap="YlOrRd",aspect='auto',vmin=np.min(heatmap_res),vmax=np.max(heatmap_res))
        plt.xticks(ticks = [0, 50, 100, 150, 200, 250, 300],labels=["1","5000", "10000","15000", "20000","25000",  "30000"]) 
        plt.yticks([])
        plt.tick_params(labelsize=20)

def draw(count, positions, heatmap_positions, heatmap_counts, continent, month, num_sample):
    """
    各大洲各个月的频率散点图、基因结构图、突变热点图、频率位于0-0.2的位点的频率分布直方图。

    :param count: 位点频率list
    :param positions:  位点list
    :param heatmap_positions: 频率位于1%-5%的位点list
    :param heatmap_counts: 频率位于1%-5%的位点的频率list
    :param continent: 大洲(例如: Africa)
    :param month: 月份(例如: 202005)
    :param num_sample: 样本数
    """
    # 设定宽和高
    fig = plt.figure(figsize=(60, 20))
    # plt.figure()
    grid = plt.GridSpec(20, 1, hspace=0.8, right = 0.8)
    # 设定标题
    # plt.suptitle("{}-{}-{}".format(continent, month, num_sample), fontsize=20)
    # plt.subplots_adjust(top=0.85)
    #x数据集和y数据集
    plt.subplot(grid[0:13,0])
    xpoints = np.array(positions)
    ypoints = np.array(count)

    # 根据频率设置颜色和数据值
    # plt.subplot2grid((1, 5), (0, 0), colspan=3)
    plt.title('Scattergram-' + "{}-{}-{}".format(continent, month, num_sample), fontsize = 32)
    o1 = plt.scatter(xpoints, ypoints, marker='o', c='grey', label="low mutations (frequency < 1%)")
    have_o2 = False
    for x, y in zip(xpoints, ypoints):
        if y >= 0.01 and y < 0.05:
            # plt.annotate(x, (x, y), textcoords="offset points",
            #              xytext=(0, 10), ha='center')
            o2 = plt.scatter(x, y, marker='o', c='royalblue', label="middle mutations (1% ≤ frequency < 5%)")
            have_o2 = True
        elif y >= 0.05:
            # plt.annotate(x, (x, y), textcoords="offset points",
            #              xytext=(0, 10), ha='center')
            o3 = plt.scatter(x, y, marker='o', c='r', label = "high mutations (frequency ≥ 5%)")
    plt.xlim([0, 30000])
    plt.ylim([0, 1])
    # y轴名字
    plt.ylabel("Mutation Frequency", fontsize=32)
    # produce a legend with a cross section of sizes from the scatter
    if have_o2:
        plt.legend((o1, o2, o3),("low mutations (frequency < 1%)",'middle mutations (1% ≤ frequency < 5%)',"high mutations (frequency ≥ 5%)"),fontsize=20,loc=2,bbox_to_anchor=(1.005,1),borderaxespad = 0.2, labelspacing=1)
    else:
        plt.legend((o1, o3),("low mutations (frequency < 1%)","high mutations (frequency ≥ 5%)"),fontsize=20,loc=2,bbox_to_anchor=(1.05,1),borderaxespad = 0.2, labelspacing=1)
    plt.tick_params(labelsize=20)
    # x轴名字
    # plt.xlabel("Position", fontsize=16)

    ax = plt.subplot(grid[14,0])
    # plt.subplots_adjust(bottom=0.5)
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cbar = plt.colorbar(
        mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
        cax=ax,
        ticks=[1, 30000],
        spacing='proportional',
        orientation='horizontal',
    )
    cbar.ax.tick_params(labelsize=20)
    # create a patch (proxy artist) for every color 
    patches = [ mpatches.Patch(color=legend_colors[i], label=legend_labels[i]) for i in range(len(legend_labels)) ]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, fontsize=20,bbox_to_anchor=(1.02,0),loc=3,borderaxespad = 0.2, labelspacing=1 )

    fre_arr = [0.01, 0.02, 0.03, 0.04, 0.05, 1.01]

    heatmap_draw(grid, 15, 0.01, 0.05, heatmap_positions, heatmap_counts, continent, month, num_sample)

    for i in range(5):
        heatmap_draw(grid, 16+i, fre_arr[i], fre_arr[i+1], heatmap_positions, heatmap_counts, continent, month, num_sample)

    # ax = plt.subplot(grid[15,0])
    # # plt.subplots_adjust(bottom=0.5)
    # heatmap_res = []
    # res = []
    # left_index = 1
    # right_index = 100
    # for index in range(300):
    #     temp = 0
    #     position = ""
    #     range_str = str(left_index) + ".." + str(right_index)
    #     for i, pos in enumerate(heatmap_positions):
    #         if pos >= left_index and pos <= right_index:
    #             gene = ""
    #             for j in range(len(bounds)-1):
    #                 left, right = bounds[j], bounds[j+1]
    #                 if left<=pos<=right:
    #                     gene = labels[j]
    #                     break
    #             position += (str(pos) + "-" + str(format(heatmap_counts[i],'.4f')) + "-" + gene +  ",")
    #             temp += 1
    #     if temp > 0:
    #         res.append({
    #             "Range":range_str,
    #             "Count":int(temp),
    #             "Position":position
    #         })
    #     heatmap_res.append(temp)
    #     left_index += 100
    #     right_index += 100
    # if len(res) > 0:
    #     res = pd.DataFrame(res)
    #     res.to_csv(csv_save_path + "heatmap-{}-{}-{}-output.tsv".format(continent, month, num_sample), index=False, header=True, sep="\t")
    # plt.imshow([heatmap_res], cmap="YlOrRd",aspect='auto',vmin=np.min(heatmap_res),vmax=np.max(heatmap_res))
    # plt.xticks(ticks = [0, 50, 100, 150, 200, 250, 300],labels=["1","5000", "10000","15000", "20000","25000",  "30000"]) 
    # plt.yticks([])
    # plt.tick_params(labelsize=20)
    # plt.colorbar()
    plt.savefig(
        scatter_save_path + "scatter-{}-{}-{}.png".format(continent, month, num_sample)
    )
    plt.close()

    plt.figure(figsize=(30, 20))
    # plt.subplot2grid((1, 5), (0, 3), colspan=2)
    plt.title('Mutation Distribution Histogram-' + "{}-{}-{}".format(continent, month, num_sample), fontsize = 20)
    # 设置频率分布直方图的分组
    bins=20
    # 设置频率（0 - 0.2）
    frequency = 0.2
    # print(frequency/bins, frequency/2*bins, frequency/(2*bins))
    arr = plt.hist(ypoints, bins,range=(0, frequency), alpha=0.5)
    for i in range(bins):
        if int(arr[0][i]) > 0:
            # print(int(arr[0][i]))
            plt.text(arr[1][i]+(frequency/(2*bins)),arr[0][i],s=str(int(arr[0][i])), size=16, horizontalalignment='center', verticalalignment='bottom')
    x_major_locator=MultipleLocator(frequency/bins)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xlim([-(frequency/(2*bins)), frequency+frequency/(2*bins)])
    plt.xlabel('Mutation Frequency', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.savefig(
        hist_save_path + "hist-{}-{}-{}.png".format(continent, month, num_sample))
    plt.close()
    plt.clf()


def draw_data(data, continent, month):
    """
    计算x数据集和y数据集, 即位点和频率

    :param data: 按照国家和月份分组后的数据集
    :param continent: 大洲
    :param month: 月份
    """
    positions = []
    heatmap_positions = []
    count = []
    # 病人总数
    num_sample = len(data["Id"].unique())
    # 根据位点分组
    # for position, group in data.groupby("Position"):
    #     positions.append(position)
    #     count.append(len(group) / num_sample)
    position_counts = data["Position"].value_counts()
    positions = position_counts.index
    heatmap_res = position_counts / num_sample
    heatmap_res = heatmap_res[(heatmap_res >= 0.01)]
    heatmap_counts = heatmap_res.values
    heatmap_positions = heatmap_res.index.values
    count = position_counts.values/num_sample
    # 画图
    draw(count, positions, heatmap_positions, heatmap_counts, continent, month, num_sample)

data = pd.read_csv(bounds_file_path, sep="\t", header=None,names=['id', 'proteinName', 'gene', 'index'])
bounds = [1]
legend_labels = ["orf1a (266..13468)","orf1b (13468..21555)"]
labels = ["5'UTR","orf1a","orf1b","NCR"]
print("read data done")
for row_index, row in data.iterrows():
    if row["gene"] == "orf1ab":
        temp = row["index"].split(",")
        for item in temp:
            index_list = item.split("..")
            for index in index_list:
                if int(index) not in bounds:
                    bounds.append(int(index))
    else:
        legend_labels.append(row["gene"] + " (" + row["index"] + ")")
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
colors = ['white', 'red','gold','white','orange','white','lawngreen','white','cyan','white','royalblue','white','salmon','white', 'crimson', 'white','purple','white','pink','white', 'slategray', 'white']
legend_colors = [c for c in colors if c != "white"]
print(bounds,len(bounds), labels, len(labels))
# print(legend_labels,len(legend_labels))
# print(legend_colors, len(legend_colors))

print("group by month and continent")
splits = os.listdir("../data/input/continent_month_split/")
for split in tqdm(splits):
    # split: continent-month.tsv
    print(split)
    group = split.split(".")[0]
    continent, month = group.split("-")
    group_data = pd.read_csv("../data/input/continent_month_split/"+split, sep="\t")
    draw_data(group_data, continent, month)

