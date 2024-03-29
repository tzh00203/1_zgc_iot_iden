import json
import os


def save_str_file(file_path, str_content):
    try:
        directory = os.path.dirname(file_path)
        # 检查目录是否存在，如果不存在则创建
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(str_content)
        print(f"文件已保存至 {file_path}")
    except Exception as e:
        print(f"保存文件时出错：{e}")


def save_dict_to_json(file_path, dict_content):
    try:
        directory = os.path.dirname(file_path)
        # 检查目录是否存在，如果不存在则创建
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(dict_content, file, indent=4, ensure_ascii=False)
        print(f"JSON 文件已保存至 {file_path}")
    except Exception as e:
        print(f"保存 JSON 文件时出错：{e}")


def save_list_to_csv(file_path, data_list):
    import csv
    # 二维列表，第一行为标题
    """
    data_list: [
        ['Name', 'Age', 'Gender'],
        ['John', 25, 'Male'],
        ['Jane', 30, 'Female'],
        ['Alice', 28, 'Female'],
    ]
    """

    # 将二维列表写入 CSV 文件
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_list)

    print(f"CSV 文件已保存为 {file_path}")
