import shutil
import os


origin_path = "/home/lsh/code/bishe/data/input/20211001_20220228"
target_path = "/home/lsh/code/bishe/data/input/merged_input"

files = os.listdir(origin_path)
for file in files:
    if os.path.isdir(os.path.join(origin_path, file)):
        origin_file = os.path.join(origin_path, file, "end.quality.fasta")
        target_file = os.path.join(target_path, file+".end.quality.fasta")
        shutil.copyfile(origin_file, target_file)
