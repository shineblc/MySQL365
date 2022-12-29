#!/bin/bash
BACKUPDIR=/root/
LOGFILE=$BACKUPDIR/mysql_logicbak.log
TIME=`date +"%Y-%m-%d %H:%M:%S"`
echo "$TIME Logical backup start..." >> $LOGFILE
python 3.py >>$LOGFILE

echo "$TIME script is end...." >> $LOGFILE

