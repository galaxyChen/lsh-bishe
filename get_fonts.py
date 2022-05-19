from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np

def get_zh_font():
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Simsun')
    return font

def get_en_font():
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    return font

def get_mix_font():
    font = FontProperties()
    font.set_family('sans-serif')
    font.set_name('Simsun')
    font.set_math_fontfamily('stix')
    return font

if __name__ == "__main__":
    print("请阅读使用说明")
    x1 = np.linspace(0.0, 5.0, 100)
    y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
    #--------------------------------------------------------------
    # 如果要显示的字符串只有英文或者只有中文：分开来设置字体
    zh_font=get_zh_font()
    en_font=get_en_font()
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(bottom=0.15, left=0.2)
    ax.plot(x1, y1)
    # 在这里使用fontproperties属性传入字体
    ax.set_xlabel('中文', fontproperties=zh_font)
    ax.set_ylabel('Damped oscillation [V]', fontproperties=en_font)
    plt.show()

    #--------------------------------------------------------------
    # 如果要显示的字符串同时包含了中文和英文：使用mix字体
    mix_font=get_mix_font()
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(bottom=0.15, left=0.2)
    ax.plot(x1, y1)
    # 在这里使用fontproperties属性传入字体
    # 特别注意英文部分需要用一个特殊的字符串括起来，表明这一段使用公式字体
    # 特殊字符串为$\mathrm{...}$， 把...换成对应的文字就行，如果包含空格则需要对空格转义
    ax.set_xlabel('中文 $\mathrm{This\ is\ text}$', fontproperties=mix_font)
    ax.set_ylabel('Damped oscillation [V]', fontproperties=mix_font)
    plt.show()

