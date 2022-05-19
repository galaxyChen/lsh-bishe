import numpy as np
import pandas as pd
from tqdm import tqdm
import os

input_file = "../data/output/new_avinput_res/linkage_amount.tsv"

data = pd.read_csv(input_file, sep="\t")

data_counts = data["Linkage_check"].value_counts(normalize=True)

result = pd.DataFrame()
result["Value"] = data_counts

result.to_csv("../data/output/new_avinput_res/linkage_counts.tsv", index=True, sep="\t")

print(data_counts)

