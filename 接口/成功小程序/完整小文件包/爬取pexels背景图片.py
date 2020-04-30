import requests
import os
from lxml import etree
# 定义url内容获取，并命名下载文件的名称(以url中的数字+.jpg)
def download_image(url):
    response = requests.get(url)
    filename = downloaddir + '/' + url.split('/')[-2] + '.jpg'
    with open(filename, 'wb')as f:
        f.write(response.content)
# 定义网页下拉的参数(这里是时间) 通过xpath获取html中对应的img块下的src
# 用for循环,依次提取图片的url 调用下载函数,下载
def get_image(url, time):
    params = {"seed": time}
    response = requests.get(url, params=params, headers={
        'Accept' :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Cookie':'__cfduid=d5c7d6581538878882a9e8410b8d300491584177675; locale=zh-CN; _ga=GA1.2.899968878.1584177679; _gid=GA1.2.905192118.1584177679; _hjid=5403fcca-edff-4dd7-9cc1-ed3569b71c08'
    })
    print(response.text)
    html_ele = etree.HTML(response.text)
    src = html_ele.xpath('//div[@class="hide-featured-badge hide-favorite-badge"]/article/a[1]/img/@src')
    for i in range(0, len(src)):
        print(src[i])
        download_image(src[i])

if __name__== '__main__':
    url ='https://www.pexels.com/zh-cn/'  # 定义图片网站url
    downloaddir = '背景图片'        #  定义文件夹名
    if not os.path.exists(downloaddir):  # 若不存在则创建
        os.mkdir(downloaddir)
    get_image(url, '2020-03-01')    # 输入时间url和时间参数