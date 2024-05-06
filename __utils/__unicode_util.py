"""  unicode 编码种类
Lu - 大写字母
Ll - 小写字母
Lt - 字母标题
Lm - 字母修饰符
Lo - 其他字母
Mn - 非间距调节标记
Mc - 间距调节标记
Me - 装饰修饰符
Nd - 十进制数字
Nl - 字母数字字符
No - 其他数字字符
Pc - 连字连接器
Pd - 破折号
Ps - 左括号
Pe - 右括号
Pi - 初始引号
Pf - 最终引号
Po - 其他标点符号
Sm - 数学符号
Sc - 货币符号
Sk - 连字符号
So - 其他符号
Zs - 空格分隔符
Zl - 行分隔符
Zp - 段落分隔符
Cc - 控制字符
Cf - 格式字符
Cs - 受限制的字符
"""

import unicodedata
import re


def unicode_calc_proportion(str_):

    count = 0
    for cha in str_:
        unicode_type = unicodedata.category(cha)
        # print(cha)
        if unicode_type in ["Cc", "Cf", "Cs", "Sc", "Lo", "So"]:
            count += 1

    return float(count/len(str_))


def hex_calc_proportion(str_):
    str_remove_hex = re.sub(r'\\x[0-9a-fA-F]{2}', '', str_)
    result = float( 1 - len(str_remove_hex) / len(str_) )
    print(str_remove_hex)

    return result


def unicode_filter(str_):

    new_str = ""
    for cha in str_:
        unicode_type = unicodedata.category(cha)
        # print(cha)
        if unicode_type in ["Cc", "Cf", "Cs", "Sc", "Lo", "So", "No", "Pi", "Pf", "Sk", "Ps", "Pe", "Po", "Sm"]:
            if cha != ".":
                cha = " "
        new_str += cha
    new_str = new_str.replace(",", " ")
    new_str = re.sub(r'\s+', ' ', new_str)
    return new_str


def punc_filter(str_):
    new_str = ""
    for cha in str_:
        unicode_type = unicodedata.category(cha)
        # print(cha)
        if unicode_type in []:
            if cha != ".":
                cha = " "
        new_str += cha
    new_str = new_str.replace(",", " ")
    new_str = re.sub(r'\s+', ' ', new_str)
    return new_str


if __name__ == "__main__":
    print("RAW DATE: \"08\\x02\\x01\\x00\\x04\\x06public\\xa2+\\x02\\x02e(\\x02\\x01\\x00\\x02\\x01\\x000\\x1f0\\x1d\\x06\\b+\\x06\\x01\\x02\\x01\\x01\\x01\\x00\\x04\\x11RouterOS RB450Gx4\"\n")
    print(hex_calc_proportion("RAW DATE: \"08\\x02\\x01\\x00\\x04\\x06public\\xa2+\\x02\\x02e(\\x02\\x01\\x00\\x02\\x01\\x000\\x1f0\\x1d\\x06\\b+\\x06\\x01\\x02\\x01\\x01\\x01\\x00\\x04\\x11RouterOS RB450Gx4\"\n"))
