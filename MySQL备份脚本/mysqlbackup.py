#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# author:不吃萝卜
# Backup with mysqldump everyday
# Backup Mysql can use on linux
import time
import datetime
import os
import conf
import smtplib
from email.mime.text import MIMEText
import re


# 返回任意一天
class Day(object):
    @staticmethod
    def any_day():
        # 按照分钟生成，最快每分钟备份一次，时间可自定义
        # today = datetime.date.today()
        dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        # utl_add_day = str(today - datetime.timedelta(days=int(add_days)))

        return dt


class MysqlBackup(object):
    def __init__(self, **kargs):
        self.__host = kargs['host']
        self.__dbname = kargs['db']
        self.__username = kargs['user']
        self.__password = kargs['passwd']
        self.__port = kargs['port']

    # mysqldump备份数据库
    def BakData(self, backup_file):
        cmd_bak = 'mysqldump -u' + self.__username + ' -p' + self.__password + ' -h' + self.__host + ' -P' + self.__port + ' ' + self.__dbname + ' --routines --events --single-transaction --master-data=2 --flush-logs ' + '> ' + backup_file + ' 2> /dev/null'
        outp = os.system(cmd_bak)
        return cmd_bak, outp

    # Linux下用tar打包压缩备份文件
    def TarData(self, date, tar_file):
        cmd_tar = 'cd ' + conf.backup_path + ' && tar zcf ' + 'dbbackup' + self.__dbname + '-' + date + '.tar.gz ' + tar_file + ' >> /dev/null 2>&1'
        outp = os.system(cmd_tar)
        return cmd_tar, outp

    @property
    def dbname(self):
        return self.__dbname


"""
class sendmail():
    def __init__(self, *args, **kargs):
        self.SMTPserver = kargs['address']
        self.sender = kargs['sender']
        self.password = kargs['password']
        self.destination = args[0]

    # 登录邮箱发送邮件
    def send(self, message):
        msg = MIMEText(message, _charset='utf-8')
        msg['Subject'] = 'Mysql Backup Failed'
        msg['From'] = self.sender
        msg['To'] = self.destination
        mailserver = smtplib.SMTP(self.SMTPserver, 25)
        mailserver.login(self.sender, self.password)
        mailserver.sendmail(self.sender, [self.destination], msg.as_string())
        mailserver.quit()
        print('send email success')
"""


# 主函数起始
def main():
    # DATA_DATE = Day.any_day(1)
    DATA_DATE = Day.any_day()
    # 发件人和收件人地址
    # MAIL_USER_ADDRESS = sendmail(*conf.note_user,**conf.contact_user)
    # 初始化需要备份的数据库类
    # for循环为了多个库备份
    for db_list in conf.conn_list:
        DB_BAK_INFO = MysqlBackup(**db_list)
        backup_file = conf.backup_path + 'dbbackup' + DB_BAK_INFO.dbname + '-' + DATA_DATE + '.sql'
        tar_file = 'dbbackup' + DB_BAK_INFO.dbname + '-' + DATA_DATE + '.sql'
        log_file = conf.backup_path + 'dbbackup' + DB_BAK_INFO.dbname + '.log'

        # 判断备份目录是否存在 不存在则创建
        if os.path.exists(conf.backup_path) is False:
            os.makedirs(conf.backup_path)
        # 保存日志
        with open(log_file, 'a') as f:

            f.write('\n\n ***********************\n')
            f.write(' * ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' *\n')
            f.write(' ***********************\n')
            # 不存在dump备份文件才备份
            if os.path.isfile(backup_file) is False:
                """只对备份的SQL文件是否存在做了判断，对于tar.gz压缩文件未做判断，如果存在即覆盖压缩"""
                # 备份
                cmd_result = DB_BAK_INFO.BakData(backup_file)
                f.write('** BACKUPCOMMAND     :' + re.sub('-p\S+', '*********', cmd_result[0]) + '\n')
                f.write('** DATABASE    : ' + DB_BAK_INFO.dbname + '\n')
                f.write('** DATA_DATE   : ' + DATA_DATE + '\n')
                f.write('** RESULT(BAK) : ' + (
                    'succeed\n' if cmd_result[1] == 0 and os.path.getsize(backup_file) > conf.db_size else 'failed\n'))
                # 验证低于5M的文件 视为备份失败，当然库很小也可以调整阀值,备份的SQL文件会成功，打包会失败，用于提醒
                if cmd_result[1] == 0 and os.path.getsize(backup_file) > conf.db_size:
                    # 备份成功后删除近七天数据
                    print('数据库', DB_BAK_INFO.dbname, "备份成功")
                    dd_sql = 'find ' + conf.backup_path + ' -name' + ' dbbackup' + DB_BAK_INFO.dbname + '-' + '*' + '.sql' + ' -ctime +' + conf.del_time + ' -exec rm {} \;';
                    os.system(dd_sql)
                    # 打包
                    tar_result = DB_BAK_INFO.TarData(DATA_DATE, tar_file)
                    f.write('** TARCOMMAND     :' + tar_result[0] + '\n')
                    f.write('** RESULT(TAR) : ' + ('succeed' if tar_result[1] == 0 else 'failed'))
                    if tar_result[1] == 0:
                        print('数据库', DB_BAK_INFO.dbname, '备份打包成功！')
                        dd_tar = 'find ' + conf.backup_path + ' -name' + ' dbbackup' + DB_BAK_INFO.dbname + '-' + '*' + '.tar.gz' + ' -ctime +' + conf.del_time + ' -exec rm {} \;';
                        os.system(dd_tar)
                    else:
                        # MAIL_USER_ADDRESS.send('Mysql备份打包失败，请核查！')
                        print('数据库', DB_BAK_INFO.dbname, '备份打包失败，请核查！')
                    """# 打包成功输出打包成功信息
                    if tar_result[1] == 0:
                        print('Mysql备份打包成功！')
                        # 也可以移除打包后的文件，稳妥起见不要移除
                        # os.remove(backup_file)
                    else:
                        # MAIL_USER_ADDRESS.send('Mysql备份打包失败，请核查！')
                        print('Mysql备份打包失败，请核查！')
                    """

                else:
                    # 未配置发送邮件，暂时注释
                    # MAIL_USER_ADDRESS.send('Mysql数据库备份失败，请核查！')
                    print('数据库', DB_BAK_INFO.dbname, 'Mysql数据库备份失败，请核查')
            else:
                f.write('** RESULT(BAK) : ' + '%s is already exists\n' % backup_file)
                print('%s 备份已存在，请先检查已经备份成功的文件，如不需要请删除重新备份\n' % backup_file)


# 程序入口
if __name__ == '__main__':
    main()
