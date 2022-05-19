import pandas as pd
import os
from tqdm import tqdm

input_dir = "/home/lsh/code/bishe/data/output/merged_output"
output_dir = "/home/lsh/code/bishe/data/input"
output_file = "snp_merged_adjusted2.tsv"

for i, dir in tqdm(enumerate(os.listdir(input_dir))):
    data = pd.read_csv(os.path.join(input_dir, dir, "final_snp_merged.tsv"), sep="\t")
    data = data[["gisaid_epi_isl", "date", "Country", "Position", "Ref", "Alt", "region"]]
    if i == 0:
        data.to_csv(os.path.join(output_dir, output_file),
        sep="\t", header=["Id", "Date", "Country", "Position", "Ref", "Alt", "Continent"], index=False)
    else:
        data.to_csv(os.path.join(output_dir, output_file),
        sep="\t", header=False, index=False, mode="a")
