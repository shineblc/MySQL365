#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# author:不吃萝卜
# 备份配置文件，单库or多库备份脚本
conn_dict = dict(host='127.0.0.1', user='root', passwd='mysql', db='-A', port='3306')
conn_dict2 = dict(host='127.0.0.1', user='root', passwd='mysql', db='t1', port='3307')
conn_list = [conn_dict, conn_dict2]
# contact_user = dict(address='smtp.163.com',sender='xxxxxx@163.com',password='xxxxxx')
# note_user = ('xxxxxx@126.com',)
backup_path = "/backup/"
del_time = '7'
db_size = 5242880
