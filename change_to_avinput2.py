import numpy as np
import pandas as pd
from tqdm import tqdm
import os

final_snp_path = "../data/output/merged_output/"
output_avinput_path = "../data/output/avinput_files/"

snp_splits = os.listdir(final_snp_path)
i = 0
line_count = 0
for split in tqdm(snp_splits):
    split_path = final_snp_path + split
    if os.path.isdir(split_path):
        snp_file_path = split_path + "/final_snp_merged.tsv"
        data = pd.read_csv(snp_file_path, sep="\t")
        result = pd.DataFrame()
        result["Reference"] = data["gisaid_epi_isl"]
        result["Reference"] = "NC_045512v2"
        result["Start position"] = data["Position"]
        result["End position"] = data["Position"]
        result["Ref"] = data["Ref"]
        result["Alt"] = data["Alt"]
        result["Id"] = data["gisaid_epi_isl"]
        result["date"] = data["date"]
        result["country"] = data["country"]
        result["Continent"] = data["region"]
        result["pango_lineage"] = data["pangolin_lineage"]
        result["GISAID_clade"] = data["GISAID_clade"]
        line_count += len(result)
        result.to_csv(output_avinput_path + "avinput_" + str(i) +".tsv", index = False, sep = "\t")
        i += 1
print(line_count)
