import numpy as np
import pandas as pd
from tqdm import tqdm
import os
from functools import partial
from collections import Counter

input_files_path = "../data/input/20211001_20220228/"
result = []

def partial_count(file_name):
    buffer = 1024 * 1024
    with open(file_name) as f:
        return sum(x.count('\n') for x in iter(partial(f.read, buffer), ''))

def quality_control(file_path, output_path, month):
    strain_count = 0
    indexs = []
    end_quality_num = 0
    line_count = partial_count(file_path)
    with open(file_path) as file:
        for i, line in enumerate(file):
            if line.startswith('>'):
                # print(i)
                indexs.append(i)
                strain_count += 1
        indexs.append(line_count)

    with open(file_path) as file:
        context = file.readlines()
        fw = open(output_path + '/end.quality.fasta', 'w')
        # print(context)
        for i in range(len(indexs) - 1):
            lines = context[indexs[i]:indexs[i+1]]
            line_length = len(lines)
            header_arr = lines[0].split('/')
            new_header = header_arr[0] + "|" + header_arr[2] + "|" + header_arr[3].strip() + "|" + header_arr[1] + "\n"
            c = Counter(lines[1].strip())
            for j in range(line_length-2):
                c.update(lines[j+2].strip())
            # print(c)
            bases_length = 0
            unknown_bases = 0
            degenerate_bases = 0
            for char in c:
                bases_length += c[char]
                if char == 'N':
                    unknown_bases = c[char]
                if char not in "ATCGN":
                    degenerate_bases += c[char]    
            if bases_length >= 29000 and unknown_bases <= 15 and degenerate_bases <= 50:
                for line in lines:
                    if line.startswith(">"):
                        fw.write(new_header)
                    else:
                        fw.write(line)
                end_quality_num += 1
    result.append({
        "month":month,
        "all sequences": len(indexs)-1,
        "qualitied sequences": end_quality_num
    })
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
            file_name = file.split('.')[1]
            file_type = file.split('.')[2]
            if file_type == 'fasta' and file_name == 'sequences':
                print(file)
                file_path = split_path + "/" + file
                quality_control(file_path, split_path, month)

result = pd.DataFrame(result)
result.to_csv(input_files_path+"quality_amount.tsv",index = False, sep = "\t")