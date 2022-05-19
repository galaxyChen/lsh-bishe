import numpy as np
import pandas as pd
from tqdm import tqdm
import os

files_path = "../data/output/merged_output/"

metadata_splits = os.listdir(files_path)
for split in tqdm(metadata_splits): 
    split_path = files_path + split
    temp_file = pd.read_csv(split_path + "/final_snp_merged.tsv", sep="\t")
    file_length = len(temp_file)
    not_null_length = len(temp_file[temp_file["gisaid_epi_isl"].notnull()])
    print(split, str(file_length-not_null_length))
    # print(temp_file[temp_file.isna().any(axis=1)])