import openpyxl
import pandas as pd
import re


def extract_status_code(response_text):
    # 使用正则表达式匹配 HTTP 响应
    match = re.match(r'HTTP/1\.1 (\d+) ', response_text)

    if match:
        status_code = match.group(1)
        return status_code
    else:
        return None


response_data = []
data_count = 0
http_count = 0
http_unfilter_list = [
    "Server:", "Set-Cookie:", "X-Powered-By:"
]

http_filter_list = [
    "Content-Type:", "HTTP/1.1", "Expires:", "Cache-Control:", "Pragma:", "Vary:",
    "Content-Security-Policy:", "Location:", ...
]


# 指定Excel文件路径
xlsx_file_path = '../../real-IoT-device-assets/1_host_data.xlsx'  # 替换为您的Excel文件路径

# 打开Excel文件
workbook = openpyxl.load_workbook(xlsx_file_path)
# sheet = workbook.active  # 或者使用sheet = workbook['Sheet1']
sheet = workbook['host_data']
idx = 1

# TODO 数据过滤规则完善：
for row in sheet.iter_rows(values_only=True):
    print(idx)
    idx += 1
    # 在这里，row 是一个包含一行数据的元组
    data_tmp = [row[4], row[5], row[3]]  # 补充row[3]为response协议
    if row[4] is None or row[5] is None:
        continue

    # 对responseData进行过滤操作
    if data_tmp[0] == "['-']":
        continue

    # 处理http/https协议的responseData
    if data_tmp[1].startswith("HTTP/1.1 ") or data_tmp[2].split("/")[-1] in ["HTTP", "HTTPS"]:
        list_tmp = data_tmp[1].split("\n")
        list_tmp_ = []
        # 将状态码为3XX和5XX的过滤掉
        if data_tmp[1].startswith("HTTP/1.1 ") and data_tmp[1][len("HTTP/1.1 ")] in ['3', '5']:
            print("\thttp bad")
            continue

        for response_id_tmp in range(len(list_tmp)):
            for filter_tmp in http_unfilter_list:
                if list_tmp[response_id_tmp].startswith(filter_tmp):
                    value_tmp = list_tmp[response_id_tmp][len(filter_tmp):]
                    if filter_tmp == "Set-Cookie:":
                        try:
                            value_tmp = re.sub(r'SESSIONID=.*?==&|&langfrombrows=.*?|&copyright=\d+-\d+', ' ', value_tmp)

                        except:
                            pass
                    list_tmp_.append(value_tmp)
        if not list_tmp_:
            continue
        data_tmp[1] = " ".join(list_tmp_)
        http_count += 1

    # 过滤处理FTP协议的response
    elif data_tmp[2].split("/")[-1] == "FTP":
        if "filezilla" in data_tmp[1].lower() or "serve-u" in data_tmp[1].lower():
            continue

    # 过滤处理TELNET协议的response
    elif data_tmp[2].split("/")[-1] == "TELNET":
        list_tmp = data_tmp[1].split("\n")
        list_tmp_ = []
        for telnet_tmp in list_tmp:
            if telnet_tmp.startswith("xff"):
                continue
            list_tmp_.append(telnet_tmp)
        if not list_tmp_:
            continue
        data_tmp[1] = " ".join(list_tmp_)

    # 对所有response作统一过滤
    data_tmp[1] = re.sub(r'<\s*p\s*>(.*?)<\s*/\s*p\s*>', ' ', data_tmp[1])
    data_tmp[1] = re.sub(r'x[0-9a-fA-F]{2}', ' ', data_tmp[1])
    data_tmp[1] = re.sub(r'\*', '', data_tmp[1])
    data_tmp[1] = re.sub(r'\b\d{1,2}:\d{1,2}(:\d{1,2})?\b', '', data_tmp[1])
    data_tmp[1] = data_tmp[1].replace(":", " ").replace("\n", " ").replace("&", " ")

    data_tmp[1] = re.sub(r'\s+', ' ', data_tmp[1])
    if data_tmp[1] == " " or data_tmp[1] is None:
        continue
    response_data.append(data_tmp)

response_data = response_data[1:]
filter_data = {
    'Response': []
}

filter_data_product = {
    'Product': []
}
# 处理每个responseData
for data in response_data:

    data_count += 1
    if type(data[1]) == list:
        data[1] = ";".join(data[1])
    filter_data['Response'].append(data[1])
    filter_data_product['Product'].append(data[0])
    print(data)

print(data_count)
print(http_count)

# 创建一个DataFrame对象
df = pd.DataFrame(filter_data)
df_product = pd.DataFrame(filter_data_product)

# 创建一个Excel writer对象
xlsx_writer = pd.ExcelWriter('../../real-IoT-device-assets/1_host_data_filter_v2.xlsx', engine='xlsxwriter')
xlsx_writer_product = pd.ExcelWriter('../../real-IoT-device-assets/1_host_data_product_v2.xlsx', engine='xlsxwriter')

# 将数据写入XLSX文件
df.to_excel(xlsx_writer, sheet_name='Sheet1', index=False)
df_product.to_excel(xlsx_writer_product, sheet_name='Sheet1', index=False)

# 保存XLSX文件
xlsx_writer._save()
xlsx_writer_product._save()

print("filter_response_xlsx file created successfully.")
