import requests
from bs4 import BeautifulSoup

# 设置搜索关键词和URL
search_query = "DIR600L"
url = f"https://cn.bing.com/search?q=dcs5000L&ensearch=1"
headers_bing = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
}
# 发送HTTP请求并获取页面内容
response = requests.get(url, headers=headers_bing)
html_content = response.text
print(html_content)
# 使用BeautifulSoup解析页面内容
soup = BeautifulSoup(html_content, "html.parser")

# 找到搜索结果列表
search_results = soup.find_all("li", class_="b_algo")

# 提取每个搜索结果的标题和链接
for result in search_results:
    title = result.find("h2").text
    link = result.find("a")["href"]
    print(f"Title: {title}")
    print(f"Link: {link}")
    print()



