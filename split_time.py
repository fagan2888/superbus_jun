# split the departure time in hours
infile = 'time_output.csv'
f = open(infile, 'r')
lines = f.readlines()
f.close()
time_list = [0] * 24
print time_list
for line in lines[1:]:
    infos = line.split(',')[7]  # 6 is onspot, 7 is off spot
    print infos
    # 2017-06-30 16:47:50
    arrive_hour = int(infos.split(' ')[1][0:2])
    # if arrive_hour < 5:
    #     arrive_hour += 24
    print arrive_hour
    for j in range(24):
        if arrive_hour == j:
            time_list[j] += 1

print time_list

# f=open('time_split_arrive_num.csv','w')
#
# for i in range(len(time_list)):
#     print time_list[i]
#     f.write(str(time_list[i])[1:-1]+'\n')
# f.close()
