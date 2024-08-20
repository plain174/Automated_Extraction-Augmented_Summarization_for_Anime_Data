import time
#你妈的写的又臭又长，虽然是我自己写的，但不加变量名不写注释，排序全12345，
#爱谁看谁看去，要改这份文件不如重写一遍，照着这个格式按输入输出搞黑盒算了
def D2I(x):
    return time.mktime(time.strptime(x,"%Y年%m月%d日"))
def I2D(x):
    return time.strftime("%Y年%m月%d日",time.localtime(x))

def NOW():
    return time.strftime("%Y-%m-%d %H:%M:%S")

'''格式
时间
排名 季数 动漫名 起始 中止 总时间 
'''
def result(text_name,mark_flag=False):
    AVG_TIME=0 #平均时间指向点
    TIME_SUM_RESULT=[]#每一年看多少部的直接结论
    TIME_POINT_TOTAL=[]#每个季度看的番
    UPDATE_TOTAL=[]#每季（自定义）的追番率
    UPDATE_SUM=0#平均追番率
    ANI_TIME_TOTAL=0#总看番时长
    ANI_AVG=0#从看番以来每天的看番时长
    ANI_DATE=[]

    m2=open(text_name,encoding='utf_8').readlines()
    m1=[]#存储看番大致估计存在的时间段
    totol_time2=0#一部番的总时长*放送平均点
    totol_time3=0#总时长
    total_time4=dict()#全部起始年份
    total_time5=dict()#全部中止年份
    total_time6=0
    total_time7=[]#追番的占比时长
    for x in range(len(m2)):
        m2[x]=m2[x].strip().split(',')
        if '日' in m2[x][0]:#导入看番估计时间点
            m1.append([m2[x][0],x])
        elif not(m2[x][0][0] in '0123456789' and m2[x][1][0] in '123456789'):
            m2[x]=[0]+m2[x]
        if len(m2[x])<7:
            m2[x]=m2[x]+[24]

        if len(m2[x])==7:
            m2[x][6]=int(m2[x][6])
            m2[x][5]=int(m2[x][5])
            m2[x].append(m2[x][5]*m2[x][6])
            totol_time2+=(D2I(m2[x][3])+D2I(m2[x][4]))/2*m2[x][7]
            totol_time3+=m2[x][7]
            total_time4[m2[x][3][:m2[x][3].find("年")]]=total_time4.get(m2[x][3][:m2[x][3].find("年")],0)+1
            total_time5[m2[x][4][:m2[x][3].find("年")]]=total_time5.get(m2[x][4][:m2[x][4].find("年")],0)+1
            ANI_DATE.append([D2I(m2[x][3]),D2I(m2[x][4])])
    AVG_TIME=I2D(totol_time2/totol_time3) #平均时间指向点



    total_time=[]
    for y in range(0,len(m1)-2,2):
            z=m2[m1[y][1]+1:m1[y+1][1]]+m2[m1[y+1][1]+1:m1[y+2][1]]
            n=[z[x][7] for x in range(len(z))]
            total_time.append(sum(n))
            time_period=m1[y][0]+'-'+m1[y+2][0]
            time_sum=str(int(sum(n)/24/12))+"季"+str(int(sum(n)/24%12))+'集'
            time_avg_period=sum(n)/24/12
            TIME_SUM_RESULT.append([time_period,time_sum,time_avg_period])
    total_time=[]
    TIME_POINT_TOTAL=[['2005年3月22日',0]]
    for y in range(len(m1)-1):
            z=m2[m1[y][1]+1:m1[y+1][1]]
            n=[z[x][7] for x in range(len(z))]
            total_time.append(sum(n))
            TIME_POINT_TOTAL.append([m1[y+1][0],sum(n)/24/12])
            #更详细版，完全按照划分的时间算
            #print(m1[y][0]+'-'+m1[y+1][0])
            #print(int(sum(n)/24/12),"季",int(sum(n)/24%12),'集')
            #print(round(sum(n)/24/(mm(m1[y+1][0])-mm(m1[y][0])),1))
            #统计追番率
            total_time8=0#局部追番占比时长
            a=D2I(m1[y][0])
            b=D2I(m1[y+1][0])
            for x in range(len(z)):
                if b>D2I(z[x][3])>a or a<D2I(z[x][4])<b:
                    total_time7.append(z[x][7])
                    total_time8+=z[x][7]
            UPDATE_TOTAL.append(total_time8/sum(n)) #局部追番占比
    UPDATE_SUM=sum(total_time7[1:])/totol_time3

    ANI_TIME_TOTAL=int(sum(total_time)/24/12),"季",int(sum(total_time)/24%12),'集'#总时长
    ANI_AVG=sum(total_time[1:])/(D2I(m1[-1][0])-D2I(m1[1][0]))/24#总一天看番率
    RE={    'AVG_TIME':AVG_TIME,
    'TIME_SUM_RESULT':TIME_SUM_RESULT,
    'TIME_POINT_TOTAL':TIME_POINT_TOTAL,
    'UPDATE_TOTAL':UPDATE_TOTAL,
    'UPDATE_SUM':UPDATE_SUM,
    'ANI_TIME_TOTAL':ANI_TIME_TOTAL,
    'ANI_AVG':ANI_AVG,
    'ANI_DATE':ANI_DATE
                }
    return RE
