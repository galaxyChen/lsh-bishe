import numpy as np
import pandas as pd
from tqdm import tqdm
import os
from functools import partial
from collections import Counter

input_files_path = "../data/input/20211001_20220228/"

def partial_count(file_name):
    buffer = 1024 * 1024
    with open(file_name) as f:
        return sum(x.count('\n') for x in iter(partial(f.read, buffer), ''))

def quality_control(file_path, output_path, month):
    strain_count = 0
    indexs = []
    end_quality_num = 0
    #line_count = partial_count(file_path)
    line_count = 0
    lines = []
    c = Counter()
    with open(file_path) as file, open(output_path + '/end.quality.fasta', 'w') as fw:
        for i, line in enumerate(file):
            if line.startswith('>'):
                if i == 0:
                    continue
                # write lines to file
                line_length = len(lines)
                header = lines[0]

                bases_length = 0
                unknown_bases = 0
                degenerate_bases = 0
                for char in c:
                    bases_length += c[char]
                    if char == 'N':
                        unknown_bases = c[char]
                    if char not in "ATCGN":
                        degenerate_bases += c[char]
                # print("unknown_bases", unknown_bases)
                # print("degenerate_bases", degenerate_bases)
                # print("bases_length", bases_length)
        
                if bases_length >= 29000 and unknown_bases <= 15 and degenerate_bases <= 50:
                    for line in lines:
                        fw.write(line)
                    end_quality_num += 1
                # print("month: ", month)
                # print("all sequence num: ", len(indexs)-1)
                # print("end quality num: ", end_quality_num)
                    
                # empty cache
                lines = []
                c = Counter()
                # print(i)
                indexs.append(i)
                strain_count += 1
            else:
                lines.append(line)
                c.update(line.strip())
            line_count += 1
        indexs.append(line_count)

    print("month: ", month)
    print("all sequence num: ", len(indexs)-1)
    print("end quality num: ", end_quality_num)
    
print("read the fasta data")
splits = os.listdir(input_files_path)
for split in tqdm(splits): 
    split_path = input_files_path + split
    if os.path.isdir(split_path):
        month = split
        files = os.listdir(split_path)
        for file in files:
            # print(file)
            file_name = file.split('.')[1]
            file_type = file.split('.')[2]
            if file_type == 'fasta' and file_name == 'sequences':
                print(file)
                file_path = split_path + "/" + file
                quality_control(file_path, split_path, month)

    # group_data = pd.read_csv(Europe_data_input_path+split, sep="\t")
    # read_data(group_data, continent, month, Europe_data_output_path, 1)
