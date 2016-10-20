---处理时间范围---
itime=`date -d "1 hour ago" +%Y%m%d`
sdaynum=0
edaynum=5
daystamp=86400
timestamp=`date -d "$itime" +%s`
start_ts=$[timestamp-daystamp*sdaynum]
end_ts=$[timestamp+daystamp*edaynum]
start_day=`date -d @${start_ts} +%Y%m%d`
end_day=`date -d @${end_ts} +%Y%m%d`
echo $start_day $end_day
