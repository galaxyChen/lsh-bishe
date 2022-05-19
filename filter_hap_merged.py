from tqdm import tqdm

data_path = "../data/input/kaks_info.tsv"
filter_file_path = "../data/input/kaks_info_filter.tsv"

delete_num = 0
filterd_num = 0
with open(data_path) as inf, open(filter_file_path, "w") as outf:
    header = inf.readline().strip()
    outf.write(header+"\t"+"Month"+"\n")
    for line in tqdm(inf):
        line = line.strip()
        date = line.split("\t")[1]
        dates = date.split("-")
        if len(dates)<=1:
            delete_num += 1
            continue
        if dates[0] == '2019':
            month = "202001"
        else:
            month = dates[0]+dates[1]
        filterd_num += 1
        outf.write("{}\t{}\n".format(line, month))
print("delete {} rows".format(delete_num))
print("filterd {} rows".format(filterd_num))
