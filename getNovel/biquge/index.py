# -*- coding: utf-8 -*
import re
import os
import time
import json
import requests
from bs4 import BeautifulSoup
from common import getUrlContent, getNovelUrlByTitle, getNovelUrlListById, getNovelContent

def main(defaultIndex=0):

    try:

        with open('./config.json') as configfile:
            data = configfile.read()

        pwd = os.getcwd()

        # 获取配置
        configData = json.loads(data)

        # 获取搜索的小说列表
        content = getUrlContent(configData['url'], configData['params'])

        # 获取小说所在的地址
        novelUrl = getNovelUrlByTitle(content, configData['params']['keyword'])

        # 获取小说网页内容
        content = getUrlContent(novelUrl)

        # 获取所有章节的地址
        sectionUrlList = getNovelUrlListById(content, "list")

        # 检测文件夹是否存在
        dirPath = pwd + "/" + configData['params']['keyword']
        folder = os.path.exists(dirPath)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(dirPath)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print("---  new folder...  ---")

        content = getUrlContent(configData['domain'] + sectionUrlList[1])
        text, title = getNovelContent(content)

        for index in range(len(sectionUrlList)):
            if(index < defaultIndex):
                continue

            filename = '/novel_' + str(int(index/100)) + '.txt'

            model = 'a'
            if(index == 0):
                model = 'w'

            with open(dirPath + filename, model) as txt:
                content = getUrlContent(configData['domain'] + sectionUrlList[index])
                text, title = getNovelContent(content)
                text = re.sub(r"\s+", '\r\n', text)
                txt.write('#### {title}\n{text}\n\n'.format(
                    title=title, text=text))
                time.sleep(0.1) # 延迟一会，不要太频繁

    except Exception as reason:
        print("发生了错误", reason, index)
        main(index)  # 再次尝试执行


if __name__ == '__main__':
    main()
