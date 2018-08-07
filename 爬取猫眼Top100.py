import requests
from requests.exceptions import RequestException
import re
import json
 
 
# 获取TOP100榜页面的URL
def get_url_links():
    base_url = 'http://maoyan.com/board/4?offset='
    list_url = []
    for i in range(10):
        new_base_url = base_url + str(i * 10)
        list_url.append(new_base_url)
    return list_url
 
 
# 获取页面的HTML代码
def get_page_code(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
 
 
# 解析HTML代码，获取每部电影的主要信息
def parse_page_code(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?<p class="name">.*?>(.*?)</a>.*?class="star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S)
    results = re.findall(pattern, html)
    for item in results:
        yield {
            'index': item[0],
            'title': item[1],
            'actor': item[2].replace('\n', '').strip()[3:],
            'time': item[3][5:],
            'score': item[4] + item[5]
        }
 
 
# 将每部电影主要信息写入文件，通过json库的dumps()方法实现字典的序列化，指定参数ensure_ascii=False保证输出结果是中文而不是Unicode编码
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
 
 
# 程序入口
def main():
    links = get_url_links()
    for i in links:
        html = get_page_code(i)
        for item in parse_page_code(html):
            write_to_file(item)
            print(item)
 
 
# 判断是否是直接运行此脚本文件
if __name__ == '__main__':
    main()