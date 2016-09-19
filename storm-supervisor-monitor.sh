#! /bin/sh
source $HOME/.bash_profile
exec_cmd=/opt/developer/storm/bin/storm
process="supervisor"

curdir=`dirname $0`
if [ $curdir = '.' ];then
    curdir=`pwd`
fi
lock=$curdir/.$process.lock
itime=`date +%s`
LogFileSize=10485760
LOG_FILE="${curdir}/log/supervisor.log"
if [ -f ${LOG_FILE} ]; then
  logfilesize=`ls -l ${LOG_FILE}|awk '{print $5}'`
  if [ ${logfilesize} -gt ${LogFileSize} ]; then
    mv $LOG_FILE $LOG_FILE.$itime  
  fi
fi

function f_send_msg()
{
    telmsg="$@"
    SENDSTR="curl -X POST -H \"Content-Type: application/json\" -d '{\"code\":24, \"desc\": \"${telmsg}\"}' http://alert.test.com/v1/alert/"
    eval "${SENDSTR}"
    rstcode=$?
    echo "## Alarm result code is ${rstcode} ##" >> $LOG_FILE
}

function checkps()
{
    while (true)
    do
        pnum=`ps -udeveloper -f |grep backtype.storm.daemon.supervisor|grep -v grep|wc -l`
        if [ $pnum -lt 1 ];then
            msginfo="`date +'%Y-%m-%d %H:%M:%S'` `hostname -i` storm $process is not running now."
            echo $msginfo >> $LOG_FILE
            nohup $exec_cmd $process &
            f_send_msg $msginfo
        else
            echo "`date +'%Y-%m-%d %H:%M:%S'` $process ok" >> $LOG_FILE
            break
        fi
        sleep 3m
    done
}

############  main #########################
if [ ! -f $lock ];then
    touch $lock
    checkps
    rm -rf $lock
fi
