# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# 第一步：抓取数据
#------------------------------------------------------------------------------
import time, json, requests
# 抓取腾讯疫情实时json数据
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
data = json.loads(requests.get(url=url).json()['data'])
print(data)
print(data.keys())

# 统计省份信息(34个省份 湖北 广东 河南 浙江 湖南 安徽....)
num = data['areaTree'][0]['children']
print(len(num))
for item in num:
    print(item['name'],end=" ")   # 不换行
else:
    print("\n")                     # 换行
    
# 显示湖北省数据
hubei = num[0]['children']
for item in hubei:
    print(item)
else:
    print("\n")

# 解析确诊数据
total_data = {}
for item in num:
    if item['name'] not in total_data:
        total_data.update({item['name']:0})
    for city_data in item['children']:
        total_data[item['name']] +=int(city_data['total']['confirm'])    
print(total_data)
# {'湖北': 48206, '广东': 1241, '河南': 1169, '浙江': 1145, '湖南': 968, ...,  '澳门': 10, '西藏': 1}

# 解析疑似数据
total_suspect_data = {}
for item in num:
    if item['name'] not in total_suspect_data:
        total_suspect_data.update({item['name']:0})
    for city_data in item['children']:
        total_suspect_data[item['name']] +=int(city_data['total']['suspect'])    
print(total_suspect_data)

# 解析死亡数据
total_dead_data = {}
for item in num:
    if item['name'] not in total_dead_data:
        total_dead_data.update({item['name']:0})
    for city_data in item['children']:
        total_dead_data[item['name']] +=int(city_data['total']['dead'])    
print(total_dead_data)

# 解析治愈数据
total_heal_data = {}
for item in num:
    if item['name'] not in total_heal_data:
        total_heal_data.update({item['name']:0})
    for city_data in item['children']:
        total_heal_data[item['name']] +=int(city_data['total']['heal'])    
print(total_heal_data)

# 解析新增确诊数据
total_new_data = {}
for item in num:
    if item['name'] not in total_new_data:
        total_new_data.update({item['name']:0})
    for city_data in item['children']:
        total_new_data[item['name']] +=int(city_data['today']['confirm']) # today    
print(total_new_data)

#------------------------------------------------------------------------------
# 第二步：存储数据至CSV文件
#------------------------------------------------------------------------------
names = list(total_data.keys())          # 省份名称
num1 = list(total_data.values())         # 确诊数据
num2 = list(total_suspect_data.values()) # 疑似数据(全为0)
num3 = list(total_dead_data.values())    # 死亡数据
num4 = list(total_heal_data.values())    # 治愈数据
num5 = list(total_new_data.values())     # 新增确诊病例
print(names)
print(num1)
print(num2)
print(num3)
print(num4)
print(num5)

# 获取当前日期命名(2020-02-13-all.csv)
n = time.strftime("%Y-%m-%d") + "-all-4db.csv"
fw = open(n, 'w', encoding='utf-8')
fw.write('province,tpye,data\n')
i = 0
while i<len(names):
    fw.write(names[i]+',confirm,'+str(num1[i])+'\n')
    fw.write(names[i]+',dead,'+str(num3[i])+'\n')
    fw.write(names[i]+',heal,'+str(num4[i])+'\n')
    fw.write(names[i]+',new_confirm,'+str(num5[i])+'\n')
    i = i + 1
else:
    print("Over write file!")
    fw.close()

#------------------------------------------------------------------------------
# 第三步：调用Seaborn绘制柱状图
#------------------------------------------------------------------------------
import time
import matplotlib
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt 

# 读取数据
n = time.strftime("%Y-%m-%d") + "-all-4db.csv"
data = pd.read_csv(n)

# 设置窗口
fig, ax = plt.subplots(1,1)
print(data['province'])

# 设置绘图风格及字体
sns.set_style("whitegrid",{'font.sans-serif':['simhei','Arial']})

# 绘制柱状图
g = sns.barplot(x="province", y="data", hue="tpye", data=data, ax=ax,
            palette=sns.color_palette("hls", 8))

# 设置Axes的标题
ax.set_title('全国疫情最新情况')

# 设置坐标轴文字方向 
ax.set_xticklabels(ax.get_xticklabels(), rotation=-60)

# 设置坐标轴刻度的字体大小
ax.tick_params(axis='x',labelsize=8)
ax.tick_params(axis='y',labelsize=8)

plt.show()
