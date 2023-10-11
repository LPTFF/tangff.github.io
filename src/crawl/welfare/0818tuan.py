import requests
import json
from datetime import datetime
import re
from bs4 import BeautifulSoup
import pytz
import base64
# 发起 get 请求
url = 'http://www.0818tuan.com/list-1-0.html'
headers = {
    'Cookie':'_ga=GA1.2.76386796.1560325128; V2EX_REFERRER="2|1:0|10:1688803282|13:V2EX_REFERRER|12:aWxvdmV5b3U=|bc1qltcqakz08kyx2htzkzx0f7xzp63vkq6r23d0sga26998c88b2c76b6cd6e16"; PB3_SESSION="2|1:0|10:1688803282|11:PB3_SESSION|36:djJleDoxLjE2Mi45Mi4yNDY6MzczNDk2NDY=|84532bc1qltcqakz08kyx2htzkzx0f7xzp63vkq6r23d0sg3f4fa7d41dd1b7890"; _gid=GA1.2.1868043241.1688910338; V2EX_LANG=zhcn; A2="2|1:0|10:1688975957|2:A2|48:OWJkNGM5YTTrEPCPrqR3YziyHVBJnibzUcQvxyeVaz7lMmFk|ea2f32bc1qltcqakz08kyx2htzkzx0f7xzp63vkq6r23d0sg549f91a6b1294ef1"; V2EX_TAB="2|1:0|10:1688975962|8:V2EX_TAB|8:dGVjaA==|dabc1qltcqakz08kyx2htzkzx0f7xzp63vkq6r23d0sge3f94c8a23062b1bcab6"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Encoding': 'utf-8' 
}
try:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    response.raise_for_status()  # 检查请求是否成功
    print('0818tuan', response)
    extracted_data = []
    if response.status_code == 200:
        # 解析响应数据
        data = response.text
        # 解析HTML
        soup = BeautifulSoup(data, 'html.parser')
        box_div = soup.find('div', id='redtag')
        # with open('./soup.html', 'w', encoding='utf-8') as f:
        #     f.write(soup.prettify())
        # with open('./box_div.html', 'w', encoding='utf-8') as f:
        #     f.write(box_div.prettify())
        if box_div:
            for article in box_div.find_all('a',class_="list-group-item"):
                if article.find('span', class_='badge badge-success red'):
                    title = article['title']
                    href = 'http://www.0818tuan.com' + article['href']
                    time_origin=article.find('span', class_='badge badge-success red').get_text().strip()
                    # 创建北京时区对象
                    beijing_tz = pytz.timezone('Asia/Shanghai')
                    # 获取当前日期
                    today = datetime.now(beijing_tz).strftime('%Y-%m-%d')
                    # 假设time_desc是您要处理的时间字符串
                    time_desc = str(time_origin)
                    # 创建带有北京时区信息的日期时间对象
                    dt = beijing_tz.localize(datetime.strptime(f'{today} {time_desc}:00', '%Y-%m-%d %H:%M:%S'))
                    # 转换为时间戳（毫秒）
                    timestamp = int(dt.timestamp() * 1000)
                    extracted_data.append({
                        'link': href,
                        'title': title,
                        'img_src': '',
                        'time': str(dt),
                        'timestamp': timestamp,
                        'website': '0818tuan',
                    })
        # 转化为JSON格式
        json_data = json.dumps(extracted_data, ensure_ascii=False, indent=4)
        # 保存为JSON文件
        with open('./src/public/data/welfare/0818tuan.json', 'w', encoding='utf-8') as file:
            file.write(json_data)
            print('0818tuan分析数据导出成功')
    else:
        print('0818tuan请求失败001')
except requests.exceptions.RequestException as e:
    print('0818tuan请求异常002:', e)
except Exception as e:
    print('0818tuan发生异常003:', e)
