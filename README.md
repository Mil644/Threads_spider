# Toopic 图片爬虫

这是一个基于 Python 的多线程图片爬虫，用于抓取 [www.toopic.cn](https://www.toopic.cn) 网站中指定分类（`dnbz`）的图片。程序通过模拟浏览器请求、解析 HTML 页面，并利用线程池并发下载图片，有效提高抓取效率。

## 功能特点

- **自动模拟浏览器**：配置完整的请求头，降低被反爬虫机制拦截的风险。
- **多线程下载**：使用 `ThreadPoolExecutor` 实现并发下载，默认线程数为 14。
- **懒加载处理**：正确提取 `data-original` 属性中的真实图片地址。
- **自动目录管理**：检查并创建 `img/` 文件夹，图片将保存至该目录。
- **简单易用**：只需运行主脚本即可开始抓取（默认抓取第 1 至 49 页）。

## 环境要求

- Python 3.6 或更高版本
- 依赖库：
  - `requests`
  - `lxml`

## 安装步骤

1. **克隆或下载本项目**  
   ```bash
   git clone https://github.com/yourusername/toopic-spider.git
   cd toopic-spider
