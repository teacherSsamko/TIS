import csv
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

summary = open(os.path.join(BASE_DIR,"data/final_summary.csv"), 'w')
sum_dic = {
    'schedule':[0,0,0],
    'rec_prod/user':[0,0,0],
    'segments/goods':[0,0,0],
    'rec_prod/user/hourly':[0,0,0],
    'TOTAL':[0,0,0]
}
for i in range(1,6):
    with open(os.path.join(BASE_DIR,f"data/summary{i}.csv"), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        reader.__next__()
        for row in reader:
            sum_dic[row[0]] = list(map(lambda a,b: a + int(b), sum_dic[row[0]], row[2:5]))
            # break
    print(sum_dic)
    # break

summary.write('labe,average,min,max\n')
for k,v in sum_dic.items():
    summary.write(f'{k},{v[0]//5},{v[1]//5},{v[2]//5}\n')

summary.close()