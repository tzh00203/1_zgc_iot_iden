import requests
from bs4 import BeautifulSoup


def bing_search(search_query):
    """
    利用bing搜索引擎, 对search query发起网络信息获取
    返回搜索结果前10的uri列表
    return: [ search_uri_1, search_uri_2, ... ]
    """

    url = f"https://cn.bing.com/search?q={search_query}&ensearch=1"
    headers_bing = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
    }

    retry_count = 3
    while retry_count > 0:
        try:
            html = requests.get(url, headers=headers_bing)

            if html.status_code == 200:
                html_content = html.text
                break
            else:
                retry_count -= 1
        except Exception:
            retry_count -= 1

    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(html_content, "html.parser")

    # 找到搜索结果列表
    search_results = soup.find_all("li", class_="b_algo")

    search_link = []
    # 提取每个搜索结果的标题和链接
    for result in search_results:
        title = result.find("h2").text
        link = result.find("a")["href"]
        search_link.append(link)
        if len(search_link) > 7:
            break

    return search_link



