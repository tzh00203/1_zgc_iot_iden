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


if __name__ == "__main__":
    print(unicode_filter("1*!1\r\n0�½\u0002\u0001\u0000\u0004\u0006public¢�¯\u0002\u0002e(\u0002\u0001\u0000\u0002\u0001\u00000�¢0�Ÿ\u0006\b+\u0006\u0001\u0002\u0001\u0001\u0001\u0000\u0004�’ZXR10 ROS Version V4.6.02D ZXR10 T64G Software, Version V2.6.02.d.16_p05 Copyright (c) 2001-2007 by ZTE Corporation Compiled Sep 6 2007, 14:24:04"))

    print(unicodedata.category("你"))
