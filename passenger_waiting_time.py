# coding:utf-8
import time
import numpy

infile = 'ctrip_data_format_time_sort.csv'
########################################################
# outfile = 'useless.csv'
outfile = 'wating_time.csv'
f = open(infile, 'r')
all_lines = f.readlines()[1:]


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
    return julian_day, hour, all_min


waiting_time_list = [[[] for i in range(24)] for j in range(61)]
passenger_num_list = [[[] for i in range(24)] for j in range(61)]
idd_list = [[[] for i in range(24)] for j in range(61)]
for line in all_lines:
    # print line
    idd = line.split(',')[0]
    service_begin_time = line.split(',')[12]  # 服务开始时间
    active_time = line.split(',')[13]  # 验票时间
    seats = int(line.split(',')[14])  # 座位数
    # print idd,service_begin_time,active_time,seats
    checkin_day, chour, checkin_min = process_timestamp(active_time)
    depart_day, dhour, depart_min = process_timestamp(service_begin_time)
    if checkin_day >= 182 and checkin_day <= 242:
        waiting_time_list[checkin_day - 182][chour - 8].append(depart_min - checkin_min)
        passenger_num_list[checkin_day - 182][chour - 8].append(seats)
        idd_list[checkin_day - 182][chour - 8].append(idd)
f = open(outfile, 'w')

hour_extra_list = [[] for i in range(24)]
for day_no, day in enumerate(waiting_time_list):  # day表示一天中的订单等待时间列表
    # print day
    # f.write(str(day)[1:-1] + '\n')  # 这里直接输出了每一天的订单等待时间
    day_extra_list = []  # 一个辅助list用来记录一天的订单按人数加权

    for hour_no, hour in enumerate(day):  # hour 是一小时中的按订单分的订单等待时间

        b = []
        p_num_hour_list = []
        # y=[a.pop(i) for i in range(len(a)) if a[i]>10]
        for order_no, order in enumerate(hour):
            if order <= 60:
                b.append(order)
                p_num_hour_list.append(passenger_num_list[day_no][hour_no][order_no])
        hour = b

        if len(hour) != 0:
            narray = numpy.array(hour)  # 订单等待时间
            parray = numpy.array(p_num_hour_list)  # 订单人数
            # 下一句因为使用mean是直接对整个矩阵求均值，不能加权?
            avg_waiting_time = numpy.sum(narray * parray) / numpy.sum(parray)  # 计算不同日期不同小时的人均等待时间

            # calculate the var
            for order_no, order in enumerate(hour):
                for j in range(p_num_hour_list[order_no]):
                    day_extra_list.append(order)
                    hour_extra_list[hour_no].append(order)
                if order > 60:
                    print 'error_order:', idd_list[day_no][hour_no][order_no]


        else:
            avg_waiting_time = 0
        # print avg_waiting_time,
        f.write(str(avg_waiting_time) + ',')
    # print ''
    print numpy.var(day_extra_list)
    f.write('\n')
    # print numpy.var(day_extra_list)
# print hour_extra_list
print '\n\n\n\n'

for i in range(20):
    print numpy.var(hour_extra_list[i])

f.write('\n')  # 区分两个矩阵
for day in passenger_num_list:
    for hour in day:
        narray = numpy.array(hour)
        hour_passenger_num = numpy.sum(narray)
        # print hour_passenger_num,
        f.write(str(hour_passenger_num) + ',')
    # print ''
    f.write('\n')
f.close()
