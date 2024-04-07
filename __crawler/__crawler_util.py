import asyncio
import requests
from bs4 import BeautifulSoup
import re
import aiohttp
import time
from colorama import Fore, Back, Style, init
import os
from functools import wraps

root_path = 'D:/0_kindofstudy/NISL/ZGC4/real-IoT-device-assets/'


def get_local_proxy():
    from urllib.request import getproxies
    proxy = getproxies()['https']
    return proxy


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}
headers_bing = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
}


# 定义Google搜索URL
def google_search(query):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    search_url = f"https://www.google.com/search?hl=en&q={query}&btnG=Search"
    while retry_count > 0:
        try:
            html = requests.get(search_url, proxies={"http": "http://{}".format(proxy)}, headers=headers)
            # 使用代理访问
            print(proxy)
            if html.status_code == 200:
                return html.text
            else:
                retry_count -= 1
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    print(f"Failed to fetch Google search results")
    return None


# 解析搜索结果并返回前三个网页的HTML
def parse_google_search_results_v1(query, cnt_response):
    response_file_path = root_path + "1_crawler_html_v2/{cnt_response}/response.txt".format(
            cnt_response=cnt_response)
    response_search_file_path = root_path + "1_crawler_html_v2/{cnt_response}/response_search.html".format(
            cnt_response=cnt_response)
    directory = os.path.dirname(response_search_file_path)
    if os.path.exists(response_file_path) and os.path.exists(response_search_file_path):
        return None

    html = google_search(query)
    xlsx_html_detail = {query: []}
    if html is not None and query is not None:
        print(Fore.GREEN + f"-------------------------{cnt_response}: google_search_success------------------------" + Style.RESET_ALL)
        soup = BeautifulSoup(html, 'html.parser')

        # 获取前三个搜索结果的URL
        search_results = soup.find_all('a')
        cnt = 0
        if not os.path.exists(directory):
            os.makedirs(directory)
        for res in search_results:
            data_ved = res.get('data-ved')
            if data_ved:
                # 使用正则表达式匹配目标字符串
                pattern = r'<a data-ved="([^"]*)" href="([^"]*)" jsname="([^"]*)"'
                matches = re.search(pattern, str(res))
                if matches:
                    if cnt >= 1:
                        break
                    # print(cnt, res)
                    href_tmp = res.get('href')
                    with open(response_search_file_path, "w", encoding="utf-8") as response_search_file:
                        response_search_file.write(href_tmp)
                    with open(response_file_path, "w", encoding="utf-8") as response_file:
                        response_file.write(query)
                    # response = requests.get(href_tmp)
                    # if response.status_code == 200:
                    #     xlsx_html_detail[query].append([href_tmp, response.text])
                    # cnt += 1

        return xlsx_html_detail

    return None


async def fetch(client, url):
    # async with client.get(url, headers=headers, proxy=get_proxy().get("proxy")) as resp:
    async with client.get(url, headers=headers, proxy=get_local_proxy()) as resp:
        assert resp.status == 200
        return await resp.text()


async def fetch4bing(client, url):
    async with client.get(url, headers=headers_bing) as resp:
        assert resp.status == 200
        return await resp.text()


def session_manager(async_function):
    @wraps(async_function)
    async def wrapped(*args, **kwargs):
        session = aiohttp.ClientSession()
        try:
            return await async_function(session=session, *args, **kwargs)
        except aiohttp.ClientError as e:
            raise e
        finally:
            await session.close()

    return wrapped


def with_retries(max_tries: int = 5, retries_sleep_second: float = 1):
    def wrapper(function):

        @wraps(function)
        @session_manager
        async def async_wrapped(*args, **kwargs):
            tries = 1
            while tries <= max_tries:
                try:
                    return await function(*args, **kwargs)
                except aiohttp.ClientError as e:
                    print(f"Function: {function.__name__} Caused AiohttpError: {str(e)}, tries: {tries}")
                    tries += 1
                    await asyncio.sleep(retries_sleep_second)
            else:
                raise TimeoutError("Reached aiohttp max tries")

        @wraps(function)
        def wrapped(*args, **kwargs):
            tries = 1
            while tries <= max_tries:
                try:
                    return function(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    print(f"Function: {function.__name__} Caused RequestsError: {str(e)}, tries: {tries}")
                    tries += 1
                    time.sleep(retries_sleep_second)
            else:
                raise TimeoutError("Reached aiohttp max tries")

        if asyncio.iscoroutinefunction(function):
            return async_wrapped
        else:
            return wrapped

    return wrapper


async def parse_google_search_results_v3(query, cnt_response):
    async with aiohttp.ClientSession() as session:
        # print(f"\n{cnt_response}-response data starts to be used: \n" + Fore.GREEN + query + Style.RESET_ALL)
        t1 = time.time()
        response_file_path = root_path + "1_crawler_html_v2/{cnt_response}/response.txt".format(
                cnt_response=cnt_response)
        response_search_file_path = root_path + "1_crawler_html_v2/{cnt_response}/response_search.html".format(
            cnt_response=cnt_response)
        directory = os.path.dirname(response_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # if os.path.exists(response_file_path) and os.path.exists(response_search_file_path):
        #     path_tmp = root_path + "1_crawler_html_v2/{cnt_response}/1.html".format(cnt_response=cnt_response)
        #     if os.path.exists(path_tmp):
        #         return
        #     print(f"{cnt_response}-webpages info start to be collected: ")
        #     html_url_tmp = open(response_search_file_path).read()
        #     print(html_url_tmp)
        #     html_tmp = await fetch(client, html_url_tmp)
        #
        #     with open(path_tmp, "w", encoding="utf-8") as html_file:
        #         html_file.write(html_tmp)
        #     print(Fore.GREEN + f"----------{cnt_response}-collected success-----------" + Style.RESET_ALL)
        #     return

        print(f"{cnt_response}-response data starts to be used: ")

        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        print(Fore.BLUE + search_url + Style.RESET_ALL)

        try:
            html = await fetch(session, search_url)
            # print(html)

            if html:
                with open(response_file_path, "w", encoding="utf-8") as response_file:
                    response_file.write(query)

                print(f"-----------------------{cnt_response}------------------"+response_file_path)

                soup = BeautifulSoup(html, 'html.parser')
                cnt_html = 0
                # 获取前三个搜索结果的URL
                search_results = soup.find_all('a')
                for res in search_results:
                    data_ved = res.get('data-ved')
                    if data_ved:
                        # 使用正则表达式匹配目标字符串
                        pattern = r'<a data-ved="([^"]*)" href="([^"]*)" jsname="([^"]*)"'
                        matches = re.search(pattern, str(res))
                        if matches:
                            if cnt_html >= 1:
                                break
                            href_tmp = res.get('href')
                            with open(response_search_file_path, "w", encoding="utf-8") as response_search_file:
                                response_search_file.write(href_tmp)
        except Exception as e:
            print(Fore.RED + f"error occurred: {e}" + Style.RESET_ALL)


@with_retries(max_tries=5, retries_sleep_second=1)
async def parse_google_search_results_v4(query, cnt_response, session: aiohttp.ClientSession()):
    # print(f"\n{cnt_response}-response data starts to be used: \n" + Fore.GREEN + query + Style.RESET_ALL)
    t1 = time.time()
    response_file_path = root_path + "1_crawler_html_v2/{cnt_response}/response.txt".format(
            cnt_response=cnt_response)
    response_search_file_path = root_path + "1_crawler_html_v2/{cnt_response}/response_search.html".format(
        cnt_response=cnt_response)
    directory = os.path.dirname(response_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # if os.path.exists(response_file_path) and os.path.exists(response_search_file_path):
    #     path_tmp = root_path + "1_crawler_html_v2/{cnt_response}/1.html".format(cnt_response=cnt_response)
    #     if os.path.exists(path_tmp):
    #         return
    #     print(f"{cnt_response}-webpages info start to be collected: ")
    #     html_url_tmp = open(response_search_file_path).read()
    #     print(html_url_tmp)
    #     html_tmp = await fetch(client, html_url_tmp)
    #
    #     with open(path_tmp, "w", encoding="utf-8") as html_file:
    #         html_file.write(html_tmp)
    #     print(Fore.GREEN + f"----------{cnt_response}-collected success-----------" + Style.RESET_ALL)
    #     return

    print(f"{cnt_response}-response data starts to be used: ")

    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    print(Fore.BLUE + search_url + Style.RESET_ALL)
    response = await session.get(search_url, proxy=get_local_proxy())
    # print(html)

    if response.status == 200:
        html = response.text()
        with open(response_file_path, "w", encoding="utf-8") as response_file:
            response_file.write(query)

        print(f"-----------------------{cnt_response}------------------"+response_file_path)

        soup = BeautifulSoup(html, 'html.parser')
        cnt_html = 0
        # 获取前三个搜索结果的URL
        search_results = soup.find_all('a')
        for res in search_results:
            data_ved = res.get('data-ved')
            if data_ved:
                # 使用正则表达式匹配目标字符串
                pattern = r'<a data-ved="([^"]*)" href="([^"]*)" jsname="([^"]*)"'
                matches = re.search(pattern, str(res))
                if matches:
                    if cnt_html >= 1:
                        break
                    href_tmp = res.get('href')
                    with open(response_search_file_path, "w", encoding="utf-8") as response_search_file:
                        response_search_file.write(href_tmp)


async def parse_bing_search_results_v1(query, cnt_response):
    async with aiohttp.ClientSession() as client:
        try:
            response_file_path = root_path + "1_crawler_html_v2/{cnt_response}/response.txt".format(
                cnt_response=cnt_response)
            response_search_file_path = root_path + "1_crawler_html_v2/{cnt_response}/response_search.html".format(
                cnt_response=cnt_response)
            directory = os.path.dirname(response_file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            #TODO : deal with after search
            if os.path.exists(response_file_path) and os.path.exists(response_search_file_path):
                return
                path_tmp = root_path + "1_crawler_html_v2/{cnt_response}/1.html".format(cnt_response=cnt_response)
                if os.path.exists(path_tmp):
                    return
                print(f"{cnt_response}-webpages info start to be collected: ")
                html_url_tmp = open(response_search_file_path).read()
                print(html_url_tmp)
                html_tmp = await fetch(client, html_url_tmp)

                with open(path_tmp, "w", encoding="utf-8") as html_file:
                    html_file.write(html_tmp)
                print(Fore.GREEN + f"----------{cnt_response}-collected success-----------" + Style.RESET_ALL)
                return

            print(f"{cnt_response}-response data starts to be used: ")

            search_url = 'https://cn.bing.com/search?q='+query.replace(' ', '+').replace('\n', '')+'&form=ANSPH1'

            print(Fore.BLUE + search_url + Style.RESET_ALL)
            html = await fetch4bing(client, search_url)
            # print(html)

            if html:
                with open(response_file_path, "w", encoding="utf-8") as response_file:
                    response_file.write(query)

                print(f"-----------------------{cnt_response}------------------"+response_file_path)

                soup = BeautifulSoup(html, 'html.parser')

                # 获取搜索结果的URL
                search_results = soup.find_all('a', class_='tilk')
                print(search_results, end="")
                print("--------------------------------------------------------")
                # res = search_results[0]
                # href_tmp = res.get('href')
                # with open(response_search_file_path, "w", encoding="utf-8") as response_search_file:
                #     response_search_file.write(href_tmp)

        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
