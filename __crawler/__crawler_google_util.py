import requests
from bs4 import BeautifulSoup
from __crawler.__crawler_utils import get_proxy, delete_proxy

headers_google = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}


def google_search(query: str, proxy: str = None, retry_count: int = 5, headers: str = None, timeout: int = 5):
    """
    使用Google搜索引擎查询关键词，返回搜索结果前10的uri列表
    :param query: str
    :param proxy: str
    :param retry_count: int
    :param headers: dict
    :param timeout: int
    :return: list
    """
    if headers is None:
        headers = headers_google
    # if proxy is None:
    #     proxy = get_proxy().get("proxy")
    url = f"https://www.google.com/search?hl=en&q={query}&btnG=Search"
    while retry_count > 0:
        try:
            html = requests.get(url, headers=headers)
            if html.status_code == 200:
                html_content = html.text
                break
            else:
                retry_count -= 1
        except Exception as e:
            print(e)
            retry_count -= 1

    # delete_proxy(proxy)
    soup = BeautifulSoup(html_content, "html.parser")
    search_results = soup.find_all("div", class_="g")
    search_link = [[], []]
    # 提取每个搜索结果的标题和链接, 并将其存储在search_link中, 返回的二维列表中0为link, 1为title
    for result in search_results:
        title = result.find("h3").text
        link = result.find("a")["href"]
        if link.startswith("http") and link not in search_link:
            search_link[0].append(link)
            search_link[1].append(title)

    return search_link


# print(google_search("TP-LINK"))
