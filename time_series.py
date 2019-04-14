import pandas as pd
import glob
import csv
from itertools import zip_longest

res = [i for i in glob.glob('input/*.csv')]
ai = len(res)
flow=[]
temperature = []
final_time = []
for i in range (ai):
    data = pd.read_csv('input/stream_{}.csv'.format(i))
    final_time.append(data['datetime'])
    data['datetime'] = pd.to_datetime(data['datetime'])
    f=[]
    t=[]
    for hour in data.datetime.dt.hour:
        f.append(data.flow[hour])
        t.append(data.temperature[hour])
    flow.append(f)
    temperature.append(t)

si = len(data['flow'])
final_flow = [0]*(si)
final_temp = [0]*(si)
temp2 = []
timefinal = [0]*(si)
for i in range (ai):
    temp1 = [0]*(si)
    for j in range (si):
        a = flow[i][j]
        final_flow[j] += a
        temp1[j] = temperature[i][j] * a
        timefinal[j] = final_time[0][j]
    temp2.append(temp1)

for i in range (ai):
    for j in range (si):
        final_temp[j] += temp2[i][j]

for j in range (si):
    final_flow [j] = round((final_flow[j]), 2)
    final_temp [j]= round((final_temp[j]/final_flow[j]),2)

final = [timefinal,final_flow, final_temp]

export_data = zip_longest(*final, fillvalue = '')
with open('output/stream_aggregate.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("datetime", "flow", "temperature"))
      wr.writerows(export_data)
myfile.close()

