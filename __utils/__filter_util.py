import re
from bs4 import BeautifulSoup


word_dictionary_path = '../_4_DER/dictionary_words'
# prepare the dictionary
dictionary_words_list = open(word_dictionary_path, "r", encoding="utf-8").read().split("\n")


def filter_format_symbol(text: str):
    format_symbol = [
        "\r", "\n", ": ", ". ", ", ", ";", "!", "=", " -", "\'"
    ]
    for symbol in format_symbol:
        text = text.replace(symbol, " ")
    # 匹配全是数字的部分
    pattern = r' \d+ '  # 使用\b匹配单词边界，\d+匹配一个或多个数字
    text = re.sub(pattern, ' ', text)  # 用空字符串替换匹配到的内容

    filtered_text = re.sub(r'\s+', ' ', text).lower()
    return filtered_text


def filter_chinese(text):
    chinese_pattern = re.compile("[\u4e00-\u9fff]+")
    filtered_text = chinese_pattern.sub('', text)
    return filtered_text


def filter_non_ascii(text):
    filtered_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return filtered_text


def filter_dictionary_list(ori_list):
    """
    :param ori_list:
    :return: clean_list that has no stop words etc.
    """
    clean_list = []
    for word in ori_list:
        if word in dictionary_words_list:
            continue
        clean_list.append(word)
    return clean_list


def filter_dictionary_string(ori_string):
    """
    :param ori_string:
    :return: clean_string that has no stop words etc.
    """
    clean_string = ori_string
    for dict_word in dictionary_words_list:
        pattern = fr' {dict_word} '  # 使用\b匹配单词边界，\d+匹配一个或多个数字
        clean_string = re.sub(pattern, ' ', clean_string)  # 用空字符串替换匹配到的内容
    return clean_string


def html_filter(html_str):

    soup = BeautifulSoup(html_str, 'html.parser')

    # 找到并删除所有的<link>标签
    for link in soup.find_all('link'):
        link.decompose()

    for link in soup.find_all('script'):
        link.decompose()

    for link in soup.find_all('style'):
        link.decompose()

    tags_to_remove = ['</html>', '</body>']
    for tag in tags_to_remove:
        for found_tag in soup.find_all(lambda tag: str(tag) == tag):
            found_tag.decompose()
