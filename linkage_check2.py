import numpy as np
import pandas as pd
from tqdm import tqdm
import os

input_files = "../data/output/merged_output/"

pos_group = ["C21618T", "G22775A", "A22786C", "C22674T", "T22200G"]
pos_num = [0 for i in range(5)]
data_num = 0

def pos_count(data):
    if data["Position"] in pos_group:    
        i = pos_group.index(data["Position"])
        pos_num[i] += 1

file_splits = os.listdir(input_files)
for split in tqdm(file_splits):
    split_path = input_files + split + "/final_snp_merged.tsv"
    data = pd.read_csv(split_path, sep="\t")
    new_data = pd.DataFrame()
    new_data["gisaid_epi_isl"] = data["gisaid_epi_isl"]
    new_data["Position"] = data["Ref"] + data["Position"].astype(str) + data["Alt"]
    new_data["Ref"] = data["Ref"]
    new_data["Alt"] = data["Alt"]

    for group, group_data in new_data.groupby("gisaid_epi_isl"):
        data_num += 1
        group_data.apply(pos_count, axis=1)

print(pos_num, data_num)