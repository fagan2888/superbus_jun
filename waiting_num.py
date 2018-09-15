#coding:utf-8
import time

infile='ctrip_data_format_time_sort.csv'
outfile='wating_num.csv'
f=open(infile,'r')
all_lines=f.readlines()[1:]
print all_lines[0]




def process_timestamp(timestamp):
    timeStamp = float(timestamp[:-3])
    timeArray = time.localtime(timeStamp)
    #date=time.strftime('%m月%d日',timeArray)对于凌晨的时间不方便进行日期的加减变化
    julian_day = int(time.strftime("%j", timeArray))
    hour=int(time.strftime('%H',timeArray))
    min=int(time.strftime('%M',timeArray))
    if hour<8:  # afternight
        hour=hour+24
        julian_day-=1
    all_min=hour*60+min
    #print 'time:',julian_day,'天',hour,'时',min,'分',all_min# 从182天（7/1）到242天（8/30）共61天
    #print''
    return julian_day,all_min

waiting_num_list=[[0]*1140 for i in range(61)]
for line in all_lines:
    #print line
    idd=line.split(',')[0]
    service_begin_time=line.split(',')[12]  # 服务开始时间
    active_time=line.split(',')[13]  # 验票时间
    seats=int(line.split(',')[14]) # 座位数
    #print idd,service_begin_time,active_time,seats
    #print 'id:',idd
    checkin_day,checkin_min=process_timestamp(active_time)
    if checkin_day>=182 and checkin_day<=242:
        for this_min in range(checkin_min-530,1140):  # 从8点50开始计算，到3：50
            waiting_num_list[checkin_day-182][this_min] += seats

    depart_day,depart_min=process_timestamp(service_begin_time)

    if depart_day>=182 and depart_day<=242:
        for this_min in range(depart_min-530,1140):
            waiting_num_list[depart_day-182][this_min] -= seats


f=open(outfile,'w')
for day in waiting_num_list:
    print day[-1]
    f.write(str(day)[1:-1]+'\n')
f.close()