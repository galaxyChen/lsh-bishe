import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import MultipleLocator

data = pd.read_csv("./snp_merged_adjusted.tsv", sep="\t")
print(data.shape[0])

result = pd.DataFrame()
result["Reference"] = data["Id"]
result["Reference"] = "NC_045512v2"
result["Start position"] = data["Position"]
result["End position"] = data["Position"]
result["Ref"] = data["Ref"]
result["Alt"] = data["Alt"]
result["Id"] = data["Id"]
result["Date"] = data["Date"]
result["Country"] = data["Country"]
result["Continent"] = data["Continent"]

result.to_csv("./avinput.tsv", index = False, header = False, sep = "\t")