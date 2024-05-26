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
    html_content = None
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

    if html_content is None:
        return [[], []]
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


def google_api_search(query: str = "USG2100 huawei", retry_count: int = 5, timeout: int = 5):
    """
    使用Google搜索引擎api查询关键词，返回搜索结果前10的uri列表
    :param query: str
    :param retry_count: int
    :param timeout: int
    :return: list
    """

    YOUR_KEY = "AIzaSyDXJHCij9rf2SAjn9OESjYZBfXIDbZ2O6s"
    cx = "13b381ee978e24fd1"

    api = f"https://customsearch.googleapis.com/customsearch/v1?key={YOUR_KEY}&q={query}&cx={cx}"

    while retry_count > 0:
        try:
            search_result = requests.get(api)
            if search_result.status_code == 200:
                search_results = eval(search_result.text)["items"]
                break
            else:
                retry_count -= 1
        except Exception as e:
            print(e)
            retry_count -= 1

    search_link = [[], []]
    # 提取每个搜索结果的标题和链接, 并将其存储在search_link中, 返回的二维列表中0为link, 1为title
    for result in search_results:
        title = result["title"]
        link = result["link"]
        if link.startswith("http") and link not in search_link:
            search_link[0].append(link)
            search_link[1].append(title)
    print(len(search_link[0]))
    return search_link
   

# print(google_api_search())
# print(google_search("TP-LINK"))
