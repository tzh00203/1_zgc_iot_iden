# import pickle
#
# from numpy import sort
#
# cnt = 0
# cnt_tmp = 0
# dic = {}
# # 从.pkl文件加载对象
# with open("data_path/ori/train_data", encoding='utf-8') as fr:
#     lines = fr.readlines()
#     sent_, tag_ = [], []
#     for line in lines:
#         if line != '\n':
#             # print(line.strip().split())
#             print(line)
#             cnt_tmp += 1
#         if line == "\n":
#
#             cnt += 1
#             if cnt_tmp not in dic:
#                 dic[cnt_tmp] = 1
#             else:
#                 dic[cnt_tmp] += 1
#             cnt_tmp = 0
#
#
# print(cnt)  # 打印加载的数据
# # dic = sorted(dic)
# # sort(dic)
# print(dic)
# print(len(dic))

print(list("huawei is a very good tool".strip()))
