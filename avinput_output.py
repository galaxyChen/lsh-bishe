import numpy as np
import pandas as pd
from tqdm import tqdm
import os

# avinput_res_path = "../data/output/avinput_res/"
# avinput_res_output_path = "../data/output/new_avinput_res/"
avinput_res_path = "../data/input/avinput_data/"
avinput_res_output_path = "../data/input/avinput_data/"

def get_aa_substitution(aa_str):
    new_str = aa_str.split(",")[0].split(":")[4].split(".")[1]
    return new_str

def get_gene(aa_str):
    new_str = aa_str.split(",")[0].split(":")[0]
    return new_str

print("run")
# avinput_res_splits = os.listdir(avinput_res_path)
# for split in tqdm(avinput_res_splits):
    # split_path = avinput_res_path + split
split_path = avinput_res_path + "test2.tsv"
# temp_pd = pd.read_csv(split_path, sep="\t", names=["line", "type", "AA_change", "reference", "start position", "end position", "Ref", "Alt", "Id", "date", "country", "Continent", "pango_lineage", "GISAID_clade"])
temp_pd = pd.read_csv(split_path, sep="\t", names=["line", "type", "AA_change", "reference", "start position", "end position", "Ref", "Alt", "Id", "date", "country", "Continent"])
for group, group_data in temp_pd.groupby(["type"]):
    if group == "nonsynonymous SNV":
        print(group)
        result = pd.DataFrame()
        result["Id"] = group_data["Id"]
        result["Position"] = group_data["start position"]
        result["Ref"] = group_data["Ref"]
        result["Alt"] = group_data["Alt"]
        result["AA_Substitution"] = group_data["AA_change"].apply(get_aa_substitution)
        result["Gene"] = group_data["AA_change"].apply(get_gene)
        result["date"] = group_data["date"]
        result["country"] = group_data["country"]
        result["Continent"] = group_data["Continent"]
        # result["pango_lineage"] = group_data["pango_lineage"]
        # result["GISAID_clade"] = group_data["GISAID_clade"]
        result.to_csv(avinput_res_output_path  + "result.tsv", index = False, sep = "\t")
