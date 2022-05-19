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

World_data_input_path = "../data/input/World_data/"
World_data_output_path = "../data/output/frequency_position_csv/World/"
Europe_data_input_path = "../data/input/Europe_data/"
Europe_data_output_path = "../data/output/frequency_position_csv/Europe/"

H12_snv = ["C241T","T445C","C3037T", "C6286T", "C14408T", "G21255C", "C22227T", "A23403G", "C26801G", "C28932T", "G29645T"]
H12_pos = [241,445,3037, 6286, 14408, 21255, 22227, 23403, 26801, 28932, 29645]
H141_snv = ["C241T","C913T", "C3037T", "C3267T", "C5388A", "C5986T", "T6954C", "G11291A", "T11296G", "C14408T", "C14676T", "C15279T", "T16176C", "A23063T", "C23271A", "A23403G", "C23604A", "C23709T", "T24506G", "G24914C", "C27972T", "G28048T", "A28111G", "G28280C", "A28281T", "T28282A", "G28881A", "G28882A", "G28883C", "C28977T"]
H141_pos = [241,913,3037,3267,5388,5986,6954, 11291,11296, 14408, 14676, 15279, 16176, 23063, 23271,23403,23604,23709, 24506, 24914, 27972, 28048, 28111, 28280,28281, 28282, 28881, 28882, 28883, 28977]
H161_pos = ["G210T", "C241T", "C3037T", "G4181T", "C6402T", "C7124T", "C8986T", "G9053T", "C10029T", "A11201G", "A11332G", "C14408T", "G15451A", "C16466T", "C19220T", "C21618G", "G21987A", "T22917G", "C22995A", "A23403G", "C23604G", "G24410A", "C25469T", "T26767C", "T27638C", "C27752T", "C27874T", "C28253A", "A28461G", "G28881T", "G28916T", "G29402T", "G29742T"]
H161_pos = [210, 241, 3037, 4181, 6402, 7124, 8986, 9053, 10029, 11201, 11332, 14408, 15451, 16466, 19220, 21618, 21987, 22917, 22995, 23403, 23604, 24410, 25469, 26767, 27638, 27752, 27874, 28253, 28461, 28881, 28916, 29402, 29742]
fre = [0.001, 0.01, 0.02, 0.03, 0.04, 0.05, 1]

def read_data(data, continent, month, output_path, type):
    """
    计算样本数、各种突变频率和突变频率分布

    :param data: 按照国家和月份分组后的数据集
    :param continent: 大洲
    :param month: 月份
    :param output_path: 输出文件保存的路径
    :param type: 1 代表包含地区和月份，2 代表包含月份
    """
    # 计算样本数
    num_sample = len(data["Id"].unique())
    snv_counts = data["SNV"].value_counts(sort=False)
    snvs = snv_counts.index
    snv_count = snv_counts.values/num_sample
    position_counts = data["Position"].value_counts(sort=False)
    positions = position_counts.index
    position_counts = position_counts.values/num_sample

    res1 = pd.DataFrame()
    res1["SNV"] = snvs
    res1["Frequency"] = snv_count
    res1["Frequency"] = res1["Frequency"].apply(lambda x: round(x, 6))
    if type == 1:
        res1.to_csv(output_path + "{}-{}-{}-snv.tsv".format(continent, month, num_sample), index = False, header = False, sep = "\t")
    elif type == 2:
        res1.to_csv(output_path + "{}-{}-snv.tsv".format(month, num_sample), index = False, header = False, sep = "\t")
    res2 = pd.DataFrame()
    res2["SNV"] = positions
    res2["Frequency"] = position_counts
    res2["Frequency"] = res2["Frequency"].apply(lambda x: round(x, 6))
    
    res3 = []
    res4 = []
    res5 = []
    for i in range(6):
        fre1, fre2 = fre[i], fre[i+1]
        temp_res = res2[(res2["Frequency"]>=fre1)&(res2["Frequency"]<fre2)]
        pos_list = temp_res['SNV'].values.tolist()
        num_1 = 0
        num_2 = 0
        pos_str_1 = ""
        pos_str_2 = ""
        num = 0
        pos_str = ""
        for pos in pos_list:
            if type == 1:
                if pos in H12_pos:
                    num_1 += 1
                    pos_str_1 = pos_str_1  + str(pos) + ","
                if pos in H141_pos:
                    num_2 += 1
                    pos_str_2 = pos_str_2  + str(pos) + ","
            elif type == 2:
                if pos in H161_pos:
                    num += 1
                    pos_str = pos_str + str(pos) + ","
        if type == 1:
            if temp_res.shape[0]> 0:
                res3.append({
                    "Range":str(fre1) + "-" + str(fre2),
                    "Count":temp_res.shape[0],
                    "Num":num_1, 
                    "Fre":num_1/temp_res.shape[0],
                    "Pos":pos_str_1
                })
                res4.append({
                    "Range":str(fre1) + "-" + str(fre2),
                    "Count":temp_res.shape[0],
                    "Num":num_2, 
                    "Fre":num_2/temp_res.shape[0],
                    "Pos":pos_str_2
                })
        elif type == 2:
            if temp_res.shape[0]> 0:
                res5.append({
                    "Range":str(fre1) + "-" + str(fre2),
                    "Count":temp_res.shape[0],
                    "Num":num, 
                    "Fre":num/temp_res.shape[0],
                    "Pos":pos_str
                })
        # print(temp_res.head())
    
    if type == 1:
        res3 = pd.DataFrame(res3)
        res4 = pd.DataFrame(res4)
        res2.to_csv(output_path + "{}-{}-{}-pos.tsv".format(continent, month, num_sample), index = False, header = False, sep = "\t")
        res3.to_csv(output_path + "{}-{}-{}-h12.tsv".format(continent, month, num_sample), index = False, header = True, sep = "\t")
        res4.to_csv(output_path + "{}-{}-{}-h141.tsv".format(continent, month, num_sample), index = False, header = True, sep = "\t")
    elif type == 2:
        res5 = pd.DataFrame(res5)
        res2.to_csv(output_path + "{}-{}-pos.tsv".format(month, num_sample), index = False, header = False, sep = "\t")
        res5.to_csv(output_path + "{}-{}-h161.tsv".format(month, num_sample), index = False, header = True, sep = "\t")
    

print("read the data from Europe")
splits = os.listdir(Europe_data_input_path)
for split in tqdm(splits):
    # split: continent-month.tsv
    group = split.split(".")[0]
    continent, month = group.split("-")
    group_data = pd.read_csv(Europe_data_input_path+split, sep="\t")
    read_data(group_data, continent, month, Europe_data_output_path, 1)

print("read the data from the world")
splits = os.listdir(World_data_input_path)
for split in tqdm(splits):
    # split: continent-month.tsv
    month = split.split(".")[0]
    group_data = pd.read_csv(World_data_input_path+split, sep="\t")
    read_data(group_data, "", month, World_data_output_path, 2)

