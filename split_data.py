from email import header
from operator import index
from os import sep
from tkinter.tix import Tree
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import MultipleLocator
from tqdm import tqdm
import sys

filter_file_path = "../data/input/snp_merged_adjusted_filter.tsv"
worldData_output_path = "../data/input/World_data/"
continent_month_output_path = "../data/input/continent_month_split/"
Europe_output_path = "../data/input/Europe_data/"

print("reading argv")
print("Split Type:", sys.argv[1])
arg = sys.argv[1]

print("reading data")
data = pd.read_csv(filter_file_path, sep="\t")

if arg == "--w":
    print("group by month")
    for group, group_data in tqdm(data.groupby(["Month"])):
        print(group)
        group_data.to_csv(worldData_output_path + "{}.tsv".format(group), index=False, header=True, sep="\t")
elif arg == "--cm":
    print("group by month and continent")
    for group, group_data in tqdm(data.groupby(["Continent","Month"])):
        print(group[0], group[1])
        group_data.to_csv(continent_month_output_path + "{}-{}.tsv".format(group[0], group[1]), index=False, header=True, sep="\t")
elif arg == "--e":
    print("group by month and continent in Europe")
    for group, group_data in tqdm(data.groupby(["Continent","Month"])):
        print(group[0], group[1])
        if group[0] == "Europe":
            group_data.to_csv(Europe_output_path + "Europe-{}.tsv".format(group[1]), index=False, header=True, sep="\t")

