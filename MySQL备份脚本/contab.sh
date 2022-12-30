#!/bin/sh
BACKUPDIR=/root/
LOGFILE=$BACKUPDIR/mysql_logicbak.log
TIME=`date +"%Y-%m-%d %H:%M:%S"`
echo "                                        " >> $LOGFILE
echo "########################################" >> $LOGFILE
echo "             backuping...               " >> $LOGFILE
echo "########################################" >> $LOGFILE
echo "$TIME Logical backup start..." >> $LOGFILE
source /etc/profile
source ~/.bash_profile
/usr/bin/python /opt/3.py >>$LOGFILE

echo "$TIME script is end...." >> $LOGFILE
