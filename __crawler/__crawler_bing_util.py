import requests
from bs4 import BeautifulSoup
from pprint import pprint

headers_bing = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
}


def bing_search(search_query):
    """
    利用bing搜索引擎, 对search query发起网络信息获取
    返回搜索结果前10的uri列表
    :return: list [ list, list ]
    """
    url = f"https://cn.bing.com/search?q={search_query}&ensearch=1"
    retry_count = 3
    while retry_count > 0:
        try:
            html = requests.get(url, headers=headers_bing)
            if html.status_code == 200:
                html_content = html.text
                break
            else:
                retry_count -= 1
        except Exception as e:
            print(e)
            retry_count -= 1

    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(html_content, "html.parser")
    # 找到搜索结果列表
    search_results = soup.find_all("li", class_="b_algo")
    search_link = [[], []]
    # 提取每个搜索结果的标题和链接, 并将其存储在search_link中, 返回的二维列表中0为link, 1为title
    for result in search_results:
        title = result.find("h2").text
        link = result.find("cite").text
        if link.startswith("http") and link not in search_link:
            search_link[0].append(link)
            search_link[1].append(title)

    return search_link


def bing_api_search(search_query: str = "usg 1100", retry_count: int = 5):
    """
    利用bing api搜索引擎, 对search query发起网络信息获取
    返回搜索结果前10的uri列表
    :return: list [ list, list ]
    """
    subscription_key = "1fc813569fce4956989059524d25e5a1"
    search_url = "https://api.bing.microsoft.com/v7.0/search"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {
        "q": search_query,
        "count": 15,
        "responseFilter": "webpages",
        "mkt": 'en-US'
        # "textDecorations": True,
        # "textFormat": "HTML"
        }
    search_results = None
    while retry_count > 0:
        try:
            response = requests.get(search_url, headers=headers, params=params)
            print(response.status_code, response.headers, response.text)
            if response.status_code == 200 and response.text is not None:
                search_results = response.json()
                break
            else:
                retry_count -= 1
        except Exception as e:
            print(e)
            retry_count -= 1

    search_link = [[], []]
    if search_results is None or "webPages" not in search_results:
        return search_link
    # 提取每个搜索结果的标题和链接, 并将其存储在search_link中, 返回的二维列表中0为link, 1为title
    for result in search_results["webPages"]["value"]:
        title = result["name"]
        link = result["url"]
        if link.startswith("http") and link[-4:] != ".pdf" and link not in search_link:
            search_link[0].append(link)
            search_link[1].append(title)

    search_link = [search_link[0][:10], search_link[1][:10]]
    return search_link


if __name__ == "__main__":
    pprint(bing_api_search())
    
