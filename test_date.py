from datetime import datetime, timedelta
import re
t=[
'2022-05-30 18:00:02',
'2022-05-31 18:00:02',
'2022-06-01 18:00:02']


y,n,t = [datetime.strptime(i,'%Y-%m-%d %H:%M:%S') for i in t]
if y<n<t:
  print(1)

