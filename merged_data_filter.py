import numpy as np
import pandas as pd
from tqdm import tqdm
import os

first_quality_output_path = "../data/input/20211001_20220228/quality_amount.tsv"
second_quality_output_path = "../data/output/merged_output/"
metadata_files_path = "../data/input/20211001_20220228/"
metadata_output_path = "../data/output/"

first_quality_data = pd.read_csv(first_quality_output_path, sep="\t")
total_sequences = first_quality_data["all sequences"].sum()
first_quality_sequences = first_quality_data["qualitied sequences"].sum()
test_first_sequences = 0
sencond_sequences = 0
false_sequences = 0
snv_num = 0

# splits = os.listdir(second_quality_output_path)
# for split in tqdm(splits):
#     split_file = second_quality_output_path+split+"/sequences_information.tsv"
#     with open(split_file) as file:
#         for line in file:
#             if line.startswith("Total genome sequences:"):
#                 temp = line.split(":")[1].strip()
#                 temp = int(temp)
#                 test_first_sequences += temp
#             if line.startswith("Pass quality control:"):
#                 temp = line.split(":")[1].strip()
#                 temp = int(temp)
#                 sencond_sequences += temp
#             if line.startswith("Not pass quality control:"):
#                 temp = line.split(":")[1].strip()
#                 temp = int(temp)
#                 false_sequences += temp
#     snp_file = pd.read_csv(second_quality_output_path+split+"/snp_merged.tsv", sep="\t")
#     snv_num += len(snp_file)

final_metadata = None
metadata_length = 0

# def concat_strain(line):
#     if line["Id"] == "NPHL":
#         new_strain = "hCoV-19/" + line["Country"] + "/" + line["Id"] + "/" + line["Date"] + "/2021"
#     elif line["Id"] == "LA-INSACOG":
#         new_strain = "hCoV-19/" + line["Country"] + "/" + line["Id"] + "/" + line["Date"] + "/2022"
#     elif line["Country"] == "Heilongjiang":
#         new_strain = "hCoV-19/" + "China/" + line["Id"] + "/" + str(int(line["Date"]))
#     else:
#         new_strain = "hCoV-19/" + line["Country"] + "/" + line["Id"] + "/" + str(int(line["Date"]))
#     return new_strain

# snp_splits = os.listdir(second_quality_output_path)
# for split in tqdm(snp_splits):
#     print(split)
#     split_path = second_quality_output_path + split
#     if os.path.isdir(split_path):
#         snp_file_path = split_path + "/snp_merged.tsv"
#         snp_data = pd.read_csv(snp_file_path, sep="\t")
#         snp_data["strain"] = snp_data.apply(concat_strain, axis=1)
#         # snp_data["strain"] = "hCoV-19/" + snp_data["Country"] + "/" + snp_data["Id"] + "/" + snp_data["Date"].astype(int).astype(str)
#         snp_data.to_csv(split_path + "/new_snp_merged.tsv", index=False, sep="\t")

def strain_split_concat(splits):
    splits_length = len(splits)
    # print(splits_length)
    new_strain = ""
    if splits_length == 4:
        new_strain = "/".join([splits[0], splits[1].title(), splits[2], splits[3]])
    elif splits_length == 5:
        print(splits)
        if splits[2] == "MH-ICMR-NIV-INSACOG-NIVHRV22":
            new_strain = "/".join([splits[0], splits[1].title(), splits[2], splits[3]])
        else:
            new_strain = "/".join([splits[0], splits[1].title(), splits[2], splits[3], splits[4]])
    else:
        if splits[1] == "India":
            new_strain = "/".join([splits[0], splits[1].title(), splits[2], splits[3]])
        print(splits_length)
        # print(splits)
    return new_strain

metadata_splits = os.listdir(metadata_files_path)
for split in tqdm(metadata_splits): 
    split_path = metadata_files_path + split
    if os.path.isdir(split_path):
        month = split
        files = os.listdir(split_path)
        for file in files:
            file_name = file.split('.')[1]
            file_type = file.split('.')[2]
            if file_type == 'tsv' and file_name == 'metadata':
                new_temp_file = None
                metadata_file_path = split_path + "/" + file
                temp_file = pd.read_csv(metadata_file_path, sep="\t")
                strain_split = temp_file["strain"].str.split("/")
                temp_file["strain"] = strain_split.apply(strain_split_concat)
                for group, group_data in temp_file.groupby(["country"]):
                    if group == "China" or group == "Taiwan":
                        group_strain_split = group_data["strain"].str.split("/")
                        group_data["strain"] = group_strain_split.apply(lambda x: "/".join([x[0], "China".title(), x[2], x[3]]))
                    if new_temp_file is None:
                        new_temp_file = group_data
                    else:
                        new_temp_file = pd.concat([new_temp_file, group_data])

                if final_metadata is None:
                    final_metadata = new_temp_file
                else:
                    final_metadata = pd.concat([final_metadata, new_temp_file])
                temp_file_length = len(new_temp_file)
                metadata_length += temp_file_length

final_metadata.to_csv(metadata_output_path + "final_metadata.tsv", index = False, sep = "\t")

final_metadata_file = pd.read_csv(metadata_output_path + "final_metadata.tsv", sep="\t")

snp_splits = os.listdir(second_quality_output_path)
for split in tqdm(snp_splits):
    split_path = second_quality_output_path + split
    if os.path.isdir(split_path):
        snp_file_path = split_path + "/new_snp_merged.tsv"
        snp_data = pd.read_csv(snp_file_path, sep="\t")
        new_snp_data = snp_data.merge(final_metadata_file, how="left", on="strain")
        new_snp_data.to_csv(split_path + "/final_snp_merged.tsv", index=False, sep="\t")


print(total_sequences, first_quality_sequences, test_first_sequences, sencond_sequences, false_sequences)
print(metadata_length)