import requests
import re
import time
import hashlib
from pathlib import Path


class BaiDu:
    """爬取百度图片.
    """

    def __init__(self, name, page):
        self.start_time = time.time()
        self.name = name
        self.page = page
        # self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&rn=60&'
        self.url = 'https://image.baidu.com/search/acjson'
        self.header = {'Host': 'image.baidu.com',
                       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 ('
                                     'KHTML, like Gecko) Chrome/88.0.4324.192 Mobile Safari/537.36',
                       'Connection': 'keep-alive',
                       'Accept-Encoding': 'gzip, deflate, br'
                       }
        self.num = 0

    def start_spider(self):
        """
        将字符串转换为查询字符串形式
        """
        pn = 0
        for i in range(int(self.page)):
            pn += 60 * i
            form_params = {'word': self.name, 'pn': pn, 'tn': 'resultjson_com', 'ipn': 'rj', 'rn': 60}

            links = self._get_requests(self.url, form_params)

            self.spider(links)

    def _get_requests(self, url, params):
        """
        发送请求
        """
        print('[INFO]: 开始发送请求：' + url)
        ret = requests.get(url, headers=self.header, params=params)

        if str(ret.status_code) == '200':
            print('[INFO]: request 200 ok :' + ret.url)
        else:
            print('[INFO]: request {}, {}'.format(ret.status_code, ret.url))

        response = ret.content.decode()
        img_links = re.findall(r'thumbURL.*?\.jpg', response)
        links = []
        # 提取url
        for link in img_links:
            links.append(link[11:])

        return links

    def _save_image(self, link):
        """
        保存图片
        """
        print('[INFO]:正在保存图片：' + link)
        m = hashlib.md5()
        m.update(link.encode())
        name = m.hexdigest()

        self.header['Host'] = 'ss1.bdstatic.com'
        ret = requests.get(link, headers=self.header)
        image_content = ret.content

        root = Path("./image")
        if not root.is_dir():  # 无文件夹时创建
            Path.mkdir(root)

        filename = './image/' + name + '.jpg'

        with open(filename, 'wb') as f:
            f.write(image_content)

        print('[INFO]:保存成功，图片名为：{}.jpg'.format(name))

    def spider(self, links):

        self.num += 1
        for i, link in enumerate(links):
            print('*' * 50)
            print(link)
            print('*' * 50)
            if link:
                time.sleep(0.5)
                self._save_image(link)

            self.num += 1

        print('一共进行了{}次请求'.format(self.num))

    def __del__(self):

        end_time = time.time()
        print('一共花费时间:{}(单位秒)'.format(end_time - self.start_time))


if __name__ == '__main__':
    baidu = BaiDu('猫', 1)
    baidu.start_spider()
