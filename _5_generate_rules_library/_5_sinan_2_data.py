import json
from openpyxl import Workbook

wb = Workbook()
sheet = wb.active

sinan_iot_assets_path = "../../real-IoT-device-assets/3_tags4NER/part-00000-89e63ac2-fac5-4f8e-a750-3b4d80e9bac9-c000.json/part-00000-89e63ac2-fac5-4f8e-a750-3b4d80e9bac9-c000.json"
response_v3_path = "../real-IoT-device-assets/1_sinan_response_v3/"
product_v3_path = "../real-IoT-device-assets/1_sinan_product_v3/"  # useless
data_new = {
    "id": [],
    "protocol": [],
    "company": [],
    "type_first": [],
    "type_second": [],
    "product_name": []
}

header = list(data_new.keys())
sheet.append(header)
protocol_dict, type_dict = {}, {}

id_cnt = 0
global data
sinan_iot_assets = open(sinan_iot_assets_path, "r", encoding="utf-8").readlines()
for line in sinan_iot_assets:
    id_cnt += 1
    pretty_json = json.loads(line)
    print(id_cnt)
    # pretty_json_1 = json.dumps(pretty_json, indent=4, ensure_ascii=False)
    # print(pretty_json_1)
    id_tmp, protocol_tmp, company_tmp, fir_cat, sec_cat, \
        product_tmp = id_cnt, pretty_json["protocol"], pretty_json["col"]["company"], pretty_json["col"]["first_cat_name"], \
        pretty_json["col"]["second_cat_name"], pretty_json["col"]["product"]
    data_new["id"].append(id_tmp), data_new["protocol"].append(protocol_tmp), data_new["company"].append(company_tmp), \
        data_new["type_first"].append(fir_cat), data_new["type_second"].append(sec_cat), data_new["product_name"].append(
        product_tmp)
    sheet.append(
        [id_tmp, protocol_tmp, company_tmp, fir_cat, sec_cat, product_tmp]
    )

    # 统计协议和类型数据种类
    if protocol_tmp not in protocol_dict:
        protocol_dict[protocol_tmp] = 1
    else:
        protocol_dict[protocol_tmp] += 1

    type_tmp = fir_cat + "-" + sec_cat
    if type_tmp not in type_dict:
        type_dict[type_tmp] = 1
    else:
        type_dict[type_tmp] += 1

    # 保存response信息
    response_tmp = {
        "header": pretty_json["header"],
        "body": pretty_json["body"]
    }
    with open(response_v3_path+"response_"+str(id_cnt), "w", encoding="utf-8") as f:
        json.dump(response_tmp, f, indent=4)

wb.save('../real-IoT-device-assets/1_sinan_assets_v3.xlsx')
print(len(protocol_dict), protocol_dict)
print(len(type_dict), type_dict)
# print(data["body"])
#
# for key, value in data.items():
#     print(key, value)
