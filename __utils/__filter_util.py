import re
from bs4 import BeautifulSoup


word_dictionary_path = '../_4_DER/dictionary_words'
# prepare the dictionary
dictionary_words_list = open(word_dictionary_path, "r", encoding="utf-8").read().split("\n")


def filter_format_symbol(text: str):
    format_symbol = [
        "\r", "\n", ": ", ". ", ", ", ";", "!", "=", " -", "\'"
    ]
    for symbol in format_symbol:
        text = text.replace(symbol, " ")
    # 匹配全是数字的部分
    pattern = r' \d+ '  # 使用\b匹配单词边界，\d+匹配一个或多个数字
    text = re.sub(pattern, ' ', text)  # 用空字符串替换匹配到的内容

    filtered_text = re.sub(r'\s+', ' ', text).lower()
    return filtered_text


def filter_chinese(text):
    chinese_pattern = re.compile("[\u4e00-\u9fff]+")
    filtered_text = chinese_pattern.sub('', text)
    return filtered_text


def filter_non_ascii(text):
    filtered_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return filtered_text


def filter_dictionary_list(ori_list):
    """
    :param ori_list:
    :return: clean_list that has no stop words etc.
    """
    clean_list = []
    for word in ori_list:
        if word in dictionary_words_list:
            continue
        clean_list.append(word)
    return clean_list


def filter_dictionary_string(ori_string):
    """
    :param ori_string:
    :return: clean_string that has no stop words etc.
    """
    clean_list = []
    for word in ori_string.split(" "):
        if word in dictionary_words_list:
            continue
        clean_list.append(word)
    clean_string = " ".join(clean_list)
    # for dict_word in dictionary_words_list:
    #     pattern = fr' {dict_word} '  # 使用\b匹配单词边界，\d+匹配一个或多个数字
    #     clean_string = re.sub(pattern, ' ', clean_string)  # 用空字符串替换匹配到的内容
    return clean_string


def html_filter(html_str):
    # print(html_str)
    http_filter_list = [
        "HTTP/", "Date:", "Content-Type:", "Content-Length:", "Last-Modified:", "Accept-Ranges:", "Content-Security-Policy:",
        "X-Content-Type-Options:", "x-xss-protection:", "Expires:", "Cache-Control:", "Pragma:", "Vary:", "Connection:",
        "Strict-Transport-Security:"
        ]
    html_list = html_str.split("\n")
    html_clean_list = []
    id_ = 0
    for line in html_list:
        flag = 1
        if line.startswith("<"):
            break
        id_ += 1
        for filter_word in http_filter_list:
            if line.startswith(filter_word):
                flag = 0
                break
        if flag == 0:
            continue
        html_clean_list.append(line.split(":")[-1])
    html_clean_list = html_clean_list + html_list[id_:]
    html_str = "\n".join(html_clean_list)
    # print(html_str)
    soup = BeautifulSoup(html_str, 'html.parser')
    # 找到并删除所有的<link>标签
    for link in soup.find_all('link'):
        link.decompose()

    for link in soup.find_all('script'):
        link.decompose()

    for link in soup.find_all('style'):
        link.decompose()

    tags_to_remove = ['</html>', '</body>']
    for tag in tags_to_remove:
        for found_tag in soup.find_all(lambda tag: str(tag) == tag):
            found_tag.decompose()
    clean_str = re.sub(r'<[^>]+>', ' ', str(soup))
    return clean_str


if __name__ == "__main__":
    print("HTTP/1.1 200 OK\r\nDate: Wed, 01 Nov 2023 22:23:55 GMT\r\nContent-Type: text/html\r\nContent-Length: 9953\r\nLast-Modified: Tue, 22 Oct 2019 03:57:55 GMT\r\nEtag: \"5dae7e43.9953\"\r\nAccept-Ranges: bytes\r\nContent-Security-Policy: img-src 'self' data:; default-src 'self' 'unsafe-inline' 'unsafe-eval'\r\nX-Content-Type-Options: nosniff\r\nX-Frame-Options: SAMEORIGIN\r\nx-xss-protection: 1; mode=block\r\nConnection: close\r\n\r\n<!DOCTYPE html>\r\n<html>\r\n    <head>\r\n        <script>\r\n            /**\r\n             * 防止浏览器缓存导致登录页的js文件加载失败\r\n             * 如果url中没有参数则为url上加上一个随机数重新加载，需要过滤cloud方式登录\r\n             * @return {[type]} [description]\r\n             */\r\n            (function(){\r\n                var href = window.location.href;\r\n                var ran = Math.round(Math.random() * 1000000000000);\r\n                if (-1 === href.indexOf('?')){\r\n                    window.location.href = href + '?_=' + ran;\r\n                } else if (-1 === href.indexOf('_=') && -1 === href.indexOf('/?')){\r\n                    window.location.href = href + '&_=' + ran;\r\n                }\r\n            })();\r\n        </script>\r\n        <meta http-equiv=\"X-UA-Compatible\" content=\"edge\" />\r\n        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\r\n        <meta content=\"favicon.ico\" itemprop=\"image\" />\r\n        <link rel=\"stylesheet\" href=\"/style/index_3ce4dc4.css\" />\r\n        <link rel=\"stylesheet\" href=\"style/color.css\" />\r\n        <title data-text=\"Text.VideoManageSystem\"></title>\r\n    </head>\r\n    <body id=\"login_body\" class=\"login_min_height_width\">\r\n        <div class=\"pluginTip\" id=\"pluginTip\">\r\n            <div class=\"pluginVersionTip\" id=\"pluginVersionTip\" data-title=\"Text.TipDbClickClose3\"></div>\r\n        </div>\r\n        <div class=\"login_fullPage login_min_height_width\">\r\n            <div class=\"login_placeHolder\">\r\n                <div class=\"login_minHeight\"></div>\r\n            </div>\r\n            <div class=\"login_form\">\r\n                <div class=\"login_header\">\r\n                    <div class=\"logo\" style=\"background-image: url(/images/logo.png);\"></div>\r\n                </div>\r\n                <form action=\"cgi-bin/main-cgi\" method=\"post\" name=\"loginForm\" id=\"loginForm\">\r\n                    <table class=\"login_table\">\r\n                        <tr class=\"login_line\">\r\n                            <td id=\"ErrorMsg\" class=\"login_msg\" colspan=\"2\">\r\n                                <span id=\"idErrorMsg\"></span>\r\n                                <span id=\"idErrorInfo\"></span>\r\n                            </td>\r\n                            <td class=\"login_right\">\r\n                                <select class=\"lanSlect\" name=\"lLan\" id=\"language\">\r\n                                </select>\r\n                            </td>\r\n                        </tr>\r\n                        <tr class=\"login_line all_login_hidden\">\r\n                            <td class=\"login_left\">\r\n                                <div class=\"login_label_div\">\r\n                                    <label class=\"login_label\" for='szUserName' data-text=\"Text.UserName\"></label>\r\n                                </div>\r\n                            </td>\r\n                            <td class=\"login_right\">\r\n                                <input type=\"text\" class=\"in_text\" name=\"szUserName\" id=\"szUserName\" autocomplete=\"off\" />\r\n                            </td>\r\n                        </tr>\r\n                        <tr class=\"login_line all_login_hidden\">\r\n                            <td class=\"login_left\">\r\n                                <div class=\"login_label_div\">\r\n                                    <label class=\"login_label\" for='szUserLoginCert' data-text=\"Text.Passwd\"></label>\r\n                                </div>\r\n                            </td>\r\n                            <td class=\"login_right\">\r\n                                <input type=password class=\"in_text nor-submit-pwd\" id=\"szUserPasswdSrc\" maxlength=\"20\" value=\"\" autocomplete=\"off\" />\r\n                                <input type=\"hidden\" name=\"szUserLoginCert\" id=\"szUserLoginCert\" />\r\n                                <!--\r\n                                <input type=\"hidden\" name=\"szUserLoginCertEx\" id=\"szUserLoginCertEx\" />\r\n                                -->\r\n                                <input type=\"hidden\" name=\"nonce\" id=\"nonce\" />\r\n                                <input type=\"hidden\" name=\"szServIpAddr\" id=\"szServIpAddr\" />\r\n                                <span class=\"forget-pass\" id=\"forgetPass\" data-text=\"Text.ForgetPass\"></span>\r\n                            </td>\r\n                        </tr>\r\n                        <!-- <tr class=\"login_line\">\r\n                            <td class=\"login_left\">\r\n                            </td>\r\n                            <td class=\"login_right login_remPwd\">\r\n                                <input type=\"checkbox\" name=\"recordPassword\" id=\"recordPassword\" class=\"login_autoLogin\" />\r\n                                <label for='autoLogin' class=\"login_autoLoginLabel\">自动登录</label>\r\n                            </td>\r\n                        </tr> -->\r\n                        <tr class=\"login_line all_login_hidden\">\r\n                            <td class=\"login_left\"></td>\r\n                            <td class=\"login_right\">\r\n                                <div id=\"wanlanid\" class=\"wanlan\">\r\n                                    <input id=\"lan\" name=\"wanlanswitch\" type=\"radio\" checked=\"checked\" value=\"1\" />\r\n                                    <label data-text=\"Text.LAN\" for=\"lan\" class=\"config-label-right-swich-lable\">\r\n                                    </label>\r\n                                    <input id=\"wan\" name=\"wanlanswitch\" type=\"radio\" value=\"0\" />\r\n                                    <label data-text=\"Text.WAN\" for=\"wan\" class=\"config-label-right-swich-lable\">\r\n                                    </label>\r\n                                </div>\r\n                                <a name=\"login\" type=\"submit\" id=\"login\" class=\"login-button noMarginLeft\">\r\n                                    <span class=\"custom-btn-left\"></span><span class=\"custom-btn-center ellipsis width70\" data-text=\"Text.Login\" data-title=\"Text.Login\"></span><span class=\"custom-btn-right\"></span>\r\n                                </a>\r\n                                <a name=\"reset\" type=\"submit\" id=\"reset\" class=\"login-button\">\r\n                                    <span class=\"custom-btn-left\"></span><span class=\"custom-btn-center ellipsis width70\" data-text=\"Text.Reset\" data-title=\"Text.Reset\"></span><span class=\"custom-btn-right\"></span>\r\n                                </a>\r\n                            </td>\r\n                        </tr>\r\n                    </table>\r\n\r\n                </form>\r\n                <div class=\"login_tips\">\r\n                    <p data-text=\"Text.SuggestResolution\"></p>\r\n                </div>\r\n                <div id=\"insecurityPasswd\" class=\"login_hidden\">\r\n                </div>\r\n            </div>\r\n        <div class=\"findPassDialog hidden\">\r\n            <div class=\"dialog-header\">\r\n                <span data-text=\"Text.ResetPass\" class=\"header-text\"></span>\r\n            </div>\r\n            <div class=\"dialog-body step1\">\r\n                <div class=\"dialog-body-main\">\r\n                    <div class=\"findPass-qrcode\">\r\n                        <div class=\"qrcode\"></div>\r\n                        <p id=\"contact\" class=\"contact-style ellipsis\"></p>\r\n                    </div>\r\n                    <div class=\"findPass-tip\">\r\n                        <p class=\"contact-style tip-header\" data-text=\"Text.TipFindPassHead\">\r\n                        </p>\r\n                        <li class=\"contact-style2 tip-UNVWeChat\" data-text=\"Text.TipFindPassWechat\">\r\n                        </li>\r\n                        <li class=\"contact-style2 tip-APPU\" data-text=\"Text.TipFindPassApp\">\r\n                        </li>\r\n                        <li class=\"contact-style2 tip-APPEZ\" data-text=\"Text.TipFindPassApp2\">\r\n                        </li>\r\n                        <li class=\"contact-style2 tip-CustomerServerHasQRCode\" data-text=\"Text.TipFindPassAppCustom\">\r\n                        </li>\r\n                    </div>\r\n                </div>\r\n                <div class=\"dialog-body-bottom\">\r\n                    <label for=\"securityCode\" class=\"label-style\" data-text=\"Text.SecurityCode2\"></label>\r\n                    <input type=\"password\" id=\"securityCode\" class=\"in_text input-width\" name=\"securityCode2\" maxlength=\"10\">\r\n                    <span id=\"tipSecurityCode\" class=\"tipSecurityCode hidden ellipsis\"></span>\r\n                </div>\r\n            </div>\r\n            <div class=\"dialog-footer\">\r\n                <a type=\"submit\" id=\"cancel\" class=\"login-button button-margin cancel step1\">\r\n                    <span class=\"custom-btn-left\"></span><span class=\"custom-btn-center ellipsis width70\" data-text=\"Text.Cancel\"></span><span\r\n                        class=\"custom-btn-right\"></span>\r\n                </a>\r\n                <a type=\"submit\" id=\"next\" class=\"login-button button-margin step1\">\r\n                    <span class=\"custom-btn-left\"></span><span class=\"custom-btn-center ellipsis width70\" data-text=\"Text.Next\"></span><span\r\n                        class=\"custom-btn-right\"></span>\r\n                </a>\r\n            </div>\r\n        </div>\r\n    </div>\r\n        <div style=\"width:0;height:0;\" id=\"loginPlugs\"></div>\r\n    </body>\r\n    <!--[if IE & (lt IE 9)]>\r\n    <script src=\"/script/plugins/json2_f4e6ebd.js\"></script>\r\n    <![endif]-->\r\n    <script src=\"/script/plugins/MD5_f913ed0.js\"></script>\r\n    <script src=\"/script/plugins/jquery-1.10.2.min_954ab71.js\"></script>\r\n    <script src=\"/script/plugins/jquery.xml2json_0bb5881.js\"></script>\r\n    <script src=\"/script/plugins/base64.min_ae031ff.js\"></script>\r\n    <script src=\"/script/common_bd26530.js\"></script>\r\n    <script src=\"/script/index_4332ff5.js\"></script>\r\n    <script src=\"/script/static_0361c54.js\"></script>\r\n    <script src=\"/script/plugins/jquery.cookie_a5283b2.js\"></script>\r\n    <script src=\"/script/plugins/excanvas_b43971b.js\"></script>\r\n    <script src=\"/script/plugins/jquery.qrcode.min_8c0b79c.js\"></script>\r\n</html>\r\n\r\n")
