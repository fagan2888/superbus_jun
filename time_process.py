# coding:utf-8
import re
import time
infile = 'ctrip_data.csv'
outfile = 'time_output.csv'
open(outfile, 'w').close()


def output(string):
    f = open(outfile, 'a')
    f.write(string)
    f.close()


f = open(infile)
f.readline()
line = f.readline()

output('id,order_time,book_depart_time,depart_time,service_begin_time,active_time,onspot_timestamp,offspot_timestamp\n')
# output('id,下单时间,下单出发时间,出发时间,服务开始时间,验票时间,出发时间戳,到达时间戳\n')

while line:
    # print line
    all_time_stamp = re.findall('(?<=,)1[4-5]\d{11}(?=,)', line)
    idd = re.findall('\d+(?=,)', line)[0]
    time_list = []
    if len(all_time_stamp) != 7:
        print 'error in length of timstamp!'
        print idd,
        print all_time_stamp
        break
    else:
        for timestamp in all_time_stamp:
            # 使用datetime方式会有时差
            # timestamp = float(timestamp[:-3])
            # dateArray = datetime.datetime.utcfromtimestamp(timestamp)
            # otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            # print otherStyleTime

            timeStamp = float(timestamp[:-3])
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            time_list.append(otherStyleTime)
    outstring = idd + ',' + ','.join(time_list)
    # print outstring
    output(outstring + '\n')
    line = f.readline()
