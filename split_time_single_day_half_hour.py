# coding:utf-8
import time

infile = 'ctrip_data_format_time_sort.csv'
outfile = 'split_time_passenger_half_hour.csv'
f = open(infile, 'r')
all_lines = f.readlines()[1:]
print all_lines[0]


def process_timestamp(timestamp):
    timeStamp = float(timestamp[:-3])
    timeArray = time.localtime(timeStamp)
    # date=time.strftime('%m月%d日',timeArray)对于凌晨的时间不方便进行日期的加减变化
    julian_day = int(time.strftime("%j", timeArray))
    hour = int(time.strftime('%H', timeArray))
    min = int(time.strftime('%M', timeArray))
    if hour < 8:  # afternight
        hour = hour + 24
        julian_day -= 1
    all_min = hour * 60 + min
    # print 'time:',julian_day,'天',hour,'时',min,'分',all_min# 从182天（7/1）到242天（8/30）共61天
    # print''
    if min >= 30:
        flag = 1
    else:
        flag = 0
    return julian_day, hour, flag



#  the origin active time
# order_num_list = [[0] * 48 for i in range(61)]
# for line in all_lines:
#     # print line
#     idd = line.split(',')[0]
#     service_begin_time = line.split(',')[12]  # 服务开始时间
#     active_time = line.split(',')[13]  # 验票时间
#     seats = int(line.split(',')[14])  # 座位数
#     # print idd,service_begin_time,active_time,seats
#     # print 'id:',idd
#     checkin_day, checkin_hour, min_flag = process_timestamp(active_time)
#     if checkin_day >= 182 and checkin_day <= 242:
#         order_num_list[checkin_day - 182][(checkin_hour - 8) * 2 + min_flag] += seats
# f = open(outfile, 'w')
# for day in order_num_list:
#     print day
#     f.write(str(day)[1:-1] + '\n')
# f.close()



# just for repeat

outfile='split_time_passenger_half_hour_service_time.csv'
order_num_list2 = [[0] * 48 for i in range(61)]
for line in all_lines:
    # print line
    idd = line.split(',')[0]
    service_begin_time = line.split(',')[12]  # 服务开始时间
    active_time = line.split(',')[13]  # 验票时间
    seats = int(line.split(',')[14])  # 座位数
    # print idd,service_begin_time,active_time,seats
    # print 'id:',idd
    checkin_day, checkin_hour, min_flag = process_timestamp(service_begin_time)
    if checkin_day >= 182 and checkin_day <= 242:
        order_num_list2[checkin_day - 182][(checkin_hour - 8) * 2 + min_flag] += seats
f = open(outfile, 'w')
for day in order_num_list2:
    print day
    f.write(str(day)[1:-1] + '\n')
f.close()

