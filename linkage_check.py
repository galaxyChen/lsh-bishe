import numpy as np
import pandas as pd
from tqdm import tqdm
import os

input_files = "../data/output/new_avinput_res/"

result = []
sample_num = 0
check_num = 0
aa_group = ["V213G", "D405N", "R408S", "T19I", "S371F"]

def linkage_check(data):
    if str(data["AA_Substitution"]) in aa_group:
        return str(data["AA_Substitution"])
    else:
        return "NA"

splits = os.listdir(input_files)
for split in tqdm(splits):
    split_path = input_files + split
    snp_data = pd.read_csv(split_path, sep="\t")
    print(snp_data.columns, split)
    for group, group_data in snp_data.groupby(["Id", "Gene"]):
        if group[1] == "S":
            # print(split, group[0],group[1])
            group_data["Linkage_Check"] = group_data.apply(linkage_check,axis=1)
            linkage_counts = group_data["Linkage_Check"].value_counts().sort_index()
            del linkage_counts["NA"]
            linkage_indexs = linkage_counts.index
            if len(linkage_indexs) > 0:
                # print(",".join(list(linkage_indexs)))
                result.append({
                    "Id":group[0],
                    "Linkage_check":",".join(list(linkage_indexs))
                })
    id_counts = snp_data["Id"].value_counts()
    print(len(id_counts))
    sample_num += len(id_counts)

result = pd.DataFrame(result)
check_num  = len(result)
result.to_csv(input_files+"linkage_amount.tsv",index = False, sep = "\t")
print(sample_num, check_num)
