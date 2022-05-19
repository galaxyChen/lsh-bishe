import numpy as np
import pandas as pd
from tqdm import tqdm
import os

input_file = "../data/output/new_avinput_res/linkage_amount.tsv"

data = pd.read_csv(input_file, sep="\t")
data_length = len(data)

aa_group = ["V213G", "D405N", "R408S", "T19I", "S371F"]

for aa in aa_group:
    data_group = data[data["Linkage_check"].str.contains(aa)]
    print(len(data_group)/data_length, len(data_group), aa)