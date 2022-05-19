import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from matplotlib.pyplot import MultipleLocator

data = pd.read_csv("../data/input/genome_list.tsv", sep="\t", header=None,names=['id', 'proteinName', 'gene', 'index'])
# print(data.head())
bounds = [1]

for row_index, row in data.iterrows():
    # print(row_index, row["gene"])
    if row["gene"] == "orf1ab":
        temp = row["index"].split(",")
        for item in temp:
            index_list = item.split("..")
            print(index_list)
            for index in index_list:
                if int(index) not in bounds:
                    bounds.append(int(index))
        # print(temp)
    else:
        temp = row["index"].split("..")
        for item in temp:
            if int(item) not in bounds:
                bounds.append(int(item))
        print(temp)
print(len(bounds))
bounds.append(30000)
colors = ['white', 'red','gold','white','orange','white','lawngreen','white','cyan','white','royalblue','white','salmon','white', 'crimson', 'white','purple','white','pink','white', 'slategray', 'white']
print(len(colors))
res = pd.DataFrame()
res["bounds"] = bounds
res["colors"] = colors
# res.to_csv("../data/input/color_map_list.tsv", index = False, header = False, sep = "\t")
fig, ax = plt.subplots(figsize=(42, 1))
fig.subplots_adjust(bottom=0.5)
cmap = mpl.colors.ListedColormap(colors)
cmap.set_over('0')
cmap.set_under('1')

# bounds = [1, 2, 4, 7, 8]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
fig.colorbar(
    mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
    cax=ax,
    ticks=bounds,
    spacing='proportional',
    orientation='horizontal',
)
plt.savefig("../data/output/test-genome.png")
plt.close()
