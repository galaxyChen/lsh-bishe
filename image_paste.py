from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

path = "./venn/"

dirs = os.listdir( path )
for file in dirs:
    if "heatmap" in file:
        image_files = []
        width = 0
        height = 0
        month = file.split("-")[1]
        heatmap_img = Image.open(path + file)
        venn_img = Image.open(path + "venn-" + month)
        heatmap_img = heatmap_img.resize((venn_img.height, venn_img.height),Image.ANTIALIAS)
        width = heatmap_img.width + venn_img.width
        height = venn_img.height
        image_files.append(venn_img)
        image_files.append(heatmap_img)
        target = Image.new('RGB', (width + 20, height), (255,255,255))
        target.paste(image_files[0], (0, 0))
        target.paste(image_files[1], (heatmap_img.width + 20, 0))
        #新建绘图对象
        draw = ImageDraw.Draw(target)
        font = ImageFont.truetype("arial.ttf", 45)
        draw.text((width/2-100,40),month.split(".")[0],font=font, fill=(0,0,0))
        target.save(path + "paste-" + month, quality=100)
        # heatmap_img_name = file
        # venn_img_name = "venn-" + month + ".png"
