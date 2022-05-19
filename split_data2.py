from email import header
from operator import index
from os import sep
from tkinter.tix import Tree
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import MultipleLocator
from tqdm import tqdm

input_file_path = '../data/input/kaks_info_filter.tsv'
split_file_path = "../data/input/"

print("reading data")
data = pd.read_csv(input_file_path, sep="\t")

print("group by continent")
for group, group_data in tqdm(data.groupby(["Continent"])):
    if (group == "Europe"):
        group_data.to_csv(split_file_path + "kaks_info_{}_filter.tsv".format(group), index=False, header=True, sep="\t")