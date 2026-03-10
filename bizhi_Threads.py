from concurrent.futures import ThreadPoolExecutor  # 导入线程池，用于并发下载
import requests          # 导入requests库，用于发送HTTP请求
from lxml import etree   # 导入lxml的etree，用于解析HTML
import os                # 导入os模块，用于文件和目录操作

class Spider:
    """图片爬虫类，封装抓取逻辑"""

    def __init__(self):
        """初始化方法：创建会话并设置请求头"""
        # 创建requests会话，可以保持连接和cookie等状态
        self.session = requests.session()
        # 设置请求头，模拟真实浏览器的访问，降低被反爬的风险
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "priority": "u=0, i",
            "referer": "https://www.toopic.cn/dnbz/?q=--81--.html&page=3",  # 引用页，模拟从该页跳转
            "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Microsoft Edge\";v=\"145\", \"Chromium\";v=\"145\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
        }

    def get_img(self, url):
        """
        抓取指定分页下的所有图片并保存到本地
        :param url: 分页的URL
        """
        # 发送GET请求获取分页的HTML内容
        response = self.session.get(url)
        # 使用lxml解析HTML文本
        html = etree.HTML(response.text)

        # 通过XPath定位所有class为"bd"的div元素，每个div包含一张图片的信息
        img_urls = html.xpath('//div[@class="bd"]')
        for tag in img_urls:
            # 从每个div中提取图片的真实地址，该地址存储在data-original属性中（懒加载）
            img_url = tag.xpath('.//img/@data-original')[0]
            # 对图片URL发起请求，下载图片的二进制数据
            response = self.session.get(img_url)
            # 构造本地文件路径：将图片URL的最后一部分作为文件名，保存在img目录下
            with open('img/%s' % img_url.split('/')[-1], 'wb') as f:
                f.write(response.content)  # 写入图片的二进制数据
                print(img_url.split('/')[-1], "下载完成")  # 打印下载成功的提示

    def main(self):
        """主方法：创建保存目录、构造URL列表、启动线程池并发下载"""
        # 检查当前目录下是否存在名为"img"的文件夹
        file_path = os.path.exists("img")
        if not file_path:
            # 如果不存在，则创建该文件夹
            os.mkdir("img")

        # 构造需要抓取的所有分页URL（第1页到第49页）
        urls = []
        for i in range(1, 50):
            url = f"https://www.toopic.cn/dnbz/?q=--81--.html&page={i}"
            urls.append(url)

        # 创建线程池，最大并发数为14
        with ThreadPoolExecutor(14) as t:
            # 遍历所有URL，将每个抓取任务提交给线程池
            for url in urls:
                # 提交任务：调用self.get_img方法，参数为url
                # t.submit会立即返回一个Future对象，但不阻塞主线程
                t.submit(self.get_img, url)

# 程序入口
if __name__ == '__main__':
    # 实例化Spider对象
    t = Spider()
    # 调用主方法开始抓取
    t.main()