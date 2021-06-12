# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 9:15
# @Author  : HUII
# @FileName: save_competition.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup

from competition.models import CompetitionInfo


def get_ah_list():
    """
    获得安徽教育厅比赛列表
    :rtype: list
    :return:
    """
    ah_url = 'http://jyt.ah.gov.cn/tsdw/gdjyc/dxsxkhjnjs/index.html'
    raw_content = requests.get(ah_url)
    raw_content.encoding = raw_content.apparent_encoding
    return parse_ah_list(raw_content.text)


def parse_ah_list(raw_content):
    """
    解析原始html获得竞赛信息标题和地址
    :param raw_content: 原始html
    :rtype: list
    :return:
    """
    soup = BeautifulSoup(raw_content, 'html.parser')
    listnews = soup.select('.listnews')[0]
    ls = listnews.select('li')
    competition_list = []
    for i in ls[::-1]:
        if i.get('class')[0] == 'lm_line':
            continue
        time = i.find('span').string
        a = i.find('a')
        title = a['title']
        url = a['href']
        competition_list.append({
            'time': time,
            'title': title,
            'url': url
        })
    return competition_list


def save_ah_competition():
    """
    保存比赛到数据库
    :return:
    """
    competition_list = get_ah_list()
    for competition in competition_list:
        if '赛项规程' not in competition['title']:
            continue
        title = competition['title']
        if '安徽' in competition['title']:
            title = title.replace('安徽省大学生创新创业教育办公室关于发布', '')
        title = title.replace('赛项规程', '')
        title = title.replace('的通知', '')
        print(f'保存{title}中')
        content = get_ah_content(competition['url']).replace('src="', 'src="http://jyt.ah.gov.cn').replace('href="/', 'href="http://jyt.ah.gov.cn/')
        CompetitionInfo.objects.update_or_create(title=title, defaults={
            'content': content,
            'host': '安徽省教育厅',
            'deliver_date': competition['time']
        })


def get_ah_content(url):
    """
    获得比赛内容
    :param url:
    :return:
    """
    content_res = requests.get(url)
    content_res.encoding = content_res.apparent_encoding
    return parse_ah_content(content_res.text)


def parse_ah_content(raw_content):
    """
    解析比赛内容
    :param raw_content:
    :return:
    """
    soup = BeautifulSoup(raw_content, 'html.parser')
    return str(soup.select('.newscontnet')[0])


if __name__ == '__main__':
    save_ah_competition()
