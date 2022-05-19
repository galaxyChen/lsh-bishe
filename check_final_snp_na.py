import pandas as pd
import os
from tqdm import tqdm

input_dir = "/home/lsh/code/bishe/data/output/merged_output"
output_dir = "/home/lsh/code/bishe/data/input"
output_file = "snp_merged_adjusted2.tsv"

for i, dir in tqdm(enumerate(os.listdir(input_dir))):
    data = pd.read_csv(os.path.join(input_dir, dir, "final_snp_merged.tsv"), sep="\t")
    nadata = data[data["date"].isna()]
    if len(nadata) != 0:
        print(dir, "na date:", len(nadata))

