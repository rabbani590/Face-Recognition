import csv
l=[]
m=[]
res=[]
with open('D:\Face-Recognition\StudentDetails\StudentDetails.csv','rt')as f1:
  data1 = csv.reader(f1)
  for row in data1:
      m.append(row[0])
print(m)

with open('D:\Face-Recognition\Attendance\Attendance_2019-06-24_12-03-51.csv','rt')as f2:
  data2 = csv.reader(f2)
  for row in data2:
      l.append(row[0])
print(l)
for i in m:
   if i not in l:
       if i!='':
           res.append(i)
print(res)



      
