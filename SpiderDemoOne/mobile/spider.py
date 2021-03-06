# -*- coding: UTF-8 -*-
'''
    爬取京东 商品评论  ... 淘宝实在不行啊
    对象 红米note7 华为畅想9
    最后分析比对
    这一页小米
'''
import requests
from urllib import request
import json
import time
import random
from multiprocessing import Pool
from pyquery import PyQuery as pq
import csv
import pandas as pd
import numpy as np
from config import *
import pymongo

# https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv22711&productId=6600216&score=0&sortType=5&page=1&pageSize=10
# https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv22711&productId=6600216&score=0&sortType=5&page=0&pageSize=10

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

client =pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
def get_url(i):
    NUM = i
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv22711&productId=6600216&score=0&sortType=5&page='+str(i)+'&pageSize=10'
    # px = request.ProxyHandler({'http':'119.101.114.166:9999'})
    # opener = request.build_opener(px)

    # r = request.Request(url,headers=headers)
    r = requests.get(url,headers = headers)
    html = r.content.decode('gbk')
    # print(html)
    html = html.replace('fetchJSON_comment98vv22711(', '')
    html = html.replace(');', '')
    # print(html)
    data = json.loads(html)
    # 获取手机特点 总结数据
    Charcter = []
    if i ==0:
        for i in data['hotCommentTagStatistics']:
            produce = {
            '特点' : i.get("name"),
            '点赞人数' : i.get("count"),
            }
            Charcter.append(produce)
            # print(produce)
        # df = pd.DataFrame(Charcter)
        # df.to_csv('TeDian.csv',index=False,mode='a+',encoding='utf-8_sig')
        print('特点写入完成！')
            # 写入字典 DICT 和fieldnames=['firstname', 'lastname'] 可以写
            # with open('TeDian.csv','w+',newline='',encoding='utf-8') as f:
            #     fieldnames = ['特点', '点赞人数']
            #     # 获得 DictWriter对象 delimiter是分隔符 默认为 "," 表头为 'firstname' 'lastname'
            #     writer = csv.DictWriter(f,delimiter=' ',fieldnames=fieldnames)
            #     # 第一次先写入表头文件
            #     writer.writeheader()
            #     for a in produce:
            #         writer.writerow(a)

    # 总页数 100

    # print(MaxPage)
    # 总评论

    ID = []
    content_note = []
    for comments in data["comments"]:
        content_note.append(pq(comments.get("content")).text()),
        for a in content_note:
            save_txt(a)
        produce = {
        'id' : comments.get("id"),
        # ID.append(id),
        'nickname' : comments.get("nickname"),
        # Nickname.append(nickname),
        'content' : pq(comments.get("content")).text(),
        # content_note.append(content),
        'time' : comments.get("creationTime"),
        'productColor' : comments.get("productColor"),
        'productSize' : comments.get("productSize"),
        'num' : comments.get("status"),
        'score' : comments.get("score"),
        'replyCount' : comments.get("replyCount"),
        'useZAN' : comments.get("usefulVoteCount"),
        }
        print(produce)
        go_db(produce)
        # ID.append(comments.get("id")),
        #
        # comments.get("nickname"),
        # pq(comments.get("content")).text(),
        # comments.get("creationTime"),
        # comments.get("productColor"),
        # comments.get("productSize"),
        # comments.get("status"),
        # comments.get("score"),
        # comments.get("replyCount"),
        # comments.get("usefulVoteCount") ,
        # ID.append(DaTa)
        # print(np.array(DaTa).shape)
        # print(id,nickname,content,time,productColor,productSize,num,score,replyCount,useZAN)
        # with open('XiaoMitext.csv','a+',newline='',encoding='utf-8') as f:
        #     # fieldnames = ['id', 'name','评论']
        #     # 获得 writer对象 delimiter是分隔符 默认为 ","
        #     writer = csv.writer(f, delimiter=' ')
        #     # writer.writeheader()
        #     # writer.writerow(["id","nickname","content","time","productColor","productSize","num","score","replyCount","useZAN"])
        #
        #     writer.writerow(ID,content_note)
    print("第{}页".format(NUM))


# 保存到csv
def save_txt(a):
    # with open('XiaoMi.txt','a+',encoding='utf-8') as f:
    #     f.write(a)
    #     f.close()
    # print("评论写入完成")
    pass

def go_db(a):
    try:
        if db[MONGO_TABLE].insert(a):
            print("存储成功")
    except Exception:
        print("存储错误")

def main():
    # 已知maxpage = 100
    for i in range(0,100):
        time.sleep(2)
        get_url(i)
    print("抓取完毕")

if __name__ =='__main__':
    main()
    # 进程池对象
    # pool = Pool()
    # pool.map(main, [i for i in range(0,100)])






