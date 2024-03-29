import _3_crawler_util
import asyncio
import openpyxl
import os
from colorama import init
import time

init()
start, end = 0, 5000
bug_list = []

# 指定Excel文件路径
root_path = '../../real-IoT-device-assets/'
xlsx_file_path = '../../real-IoT-device-assets/1_host_data_filter_v2.xlsx'  # 替换为您的Excel文件路径
response_data = []
# 打开Excel文件
workbook = openpyxl.load_workbook(xlsx_file_path)
sheet = workbook.active  # 或者使用sheet = workbook['Sheet1']

for row in sheet.iter_rows(values_only=True):
    # 在这里，row 是一个包含一行数据的元组
    data_tmp = row[0]
    response_data.append(data_tmp)
response_data = response_data[1:]


def get_html_v1():
    # 对responseData进行查询爬虫操作
    cnt_response = start
    cnt_html = 1
    t1 = time.time()
    for each_query in response_data[start:end]:
        cnt_response += 1
        # print(f"\n{cnt_response}-response data starts to be used: \n" + Fore.GREEN + each_query + Style.RESET_ALL)
        print(f"{cnt_response}-response data starts to be used: ")
        t1 = time.time()
        try:
            cnt_html = 1
            # xlsx_html_detail = {query: [html1_data, html2_data, html3_data]}
            html_data = _3_crawler_util.parse_google_search_results_v1(each_query, cnt_response)

            # for each_html in html_data[each_query]:
            #     # 将HTML字符串写入HTML文件
            #     html_file_path = "./real-IoT-device-assets/1_crawler_html_v1/{cnt_response}/{cnt_html}.html".format(
            #         cnt_response=cnt_response, cnt_html=cnt_html)
            #     directory = os.path.dirname(html_file_path)
            #     if not os.path.exists(directory):
            #         os.makedirs(directory)
            #     with open(html_file_path, "w", encoding="utf-8") as html_file:
            #         html_file.write(each_html[1])
            #         print(f"\t{cnt_response}-{cnt_html}: crawled webpage info file created, time-cost:{time.time() - t1}: {each_html[0]}; ")
            #     cnt_html += 1
        except Exception as e:
            print(f"An error occurred: {e}")
            # TODO : 出错的爬虫记录
            bug_list.append([cnt_response, cnt_html, each_query[0]])

    print("耗时：", time.time() - t1)

    # 打开文件以写入模式
    with open('bug_list.txt', 'w') as file:
        for row in bug_list:
            # 使用join将一行中的元素连接成字符串，并使用制表符分隔
            row_str = '\t'.join(map(str, row))
            # 将每一行写入文件
            file.write(row_str + '\n')


def get_html_v2():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    cnt_response = start
    for each_query in response_data[start:end]:
        cnt_response += 1
        if each_query is None:
            continue
        task = loop.create_task(_3_crawler_util.parse_google_search_results_v3(each_query, cnt_response))
        tasks.append(task)

    t1 = time.time()

    loop.run_until_complete(_3_crawler_util.parse_google_search_results_v3(response_data[end], cnt_response))

    print("aiohttp版爬虫总耗时：", time.time() - t1)


def count4undo():
    undo_cnt = end - start
    undo_cnt_html = end - start
    for idx in range(start, end):
        response_file_path = root_path + "1_crawler_html_v2/{id}/response.txt".format(
                id=idx)
        response_search_file_path = root_path + "1_crawler_html_v2/{id}/response_search.html".format(
                id=idx)
        html_path = root_path + "1_crawler_html_v2/{id}/1.html".format(id=idx)

        if os.path.exists(response_file_path) and os.path.exists(response_search_file_path):
            undo_cnt -= 1
        if os.path.exists(html_path):
            undo_cnt_html -= 1

    print(f"--------------------------{undo_cnt} file un-google-searched---------------------------")
    print(f"--------------------------{undo_cnt_html} file no webpage info   ---------------------------")
    return undo_cnt, undo_cnt_html


if __name__ == "__main__":
    get_html_v2()
    n1, n2 = count4undo()

