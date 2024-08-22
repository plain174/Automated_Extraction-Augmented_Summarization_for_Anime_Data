import result
from main import *
import overleaf
import matplotlib.pyplot as plt
import subprocess
from pyiter import it
from matplotlib.font_manager import FontProperties
import random
def Max():
    return len(cartoon_rank1)
def to_csv():
    #global cartoon_rank3
    with open(init_menu+'/save/output_result.csv','w',encoding='utf-8')as f:
        for x in cartoon_rank3:
            if type(x)==str:
                f.write(x+'\n')
            else:
                if type(x)!=list:
                    continue
                id=str(x[-1])
                x=x[:-1]+[cartoon_data[id]['放送开始'],cartoon_data[id]['播放结束'],int(cartoon_data[id]['话数'])]
                '''
                time_avg_1=it(cartoon_data[id]['ep'][:int(cartoon_data[id]['话数'])]).map(lambda x: x[2].split(":")).map(lambda y:  int(y[2])+int(y[1])*60+int(y[0])*60*24 if len(y)>1 else print(y))
                time_avg_2=int(sum(time_avg_1)/len(list(time_avg_1))/60)
                '''
                #x.append(time_avg_2)
                f.write(",".join(it(x).map(lambda x:str(x)))+'\n')
            #print(x)

def result_1():
    return result.result(init_menu+'/save/output_result.csv',True)

def result_2():
    #话数 放送星期 动画制作|播放电视台 导演 人物设定 音乐 脚本 系列构成
    m=dict()
    for x in cartoon_data.keys():
        for y in cartoon_data[x].keys():
            m[y]=m.get(y,dict())
            if type(cartoon_data[x][y])==type("1"):
                m[y][cartoon_data[x][y]]=m[y].get(cartoon_data[x][y],[])+[x]
    count=it(sorted(m['话数'],key =lambda x:int(x))).map(lambda x:[x,len(m['话数'][x])])
    count1=it(sorted(m['放送星期'],key=lambda x: len(m['放送星期'][x]))).map(lambda x:[x,len(m['放送星期'][x]),m['放送星期'][x]])
    count2=it(sorted(m['动画制作'],key=lambda x: len(m['动画制作'][x]))).filter(lambda x: len(m['动画制作'][x])>=4).map(lambda x:[x,len(m['动画制作'][x]),m['动画制作'][x]])
    #大于三以上的出列
    print(count)
    print(count1)
    print(count2)
    x=['导演' ,'系列构成' ,'人物设定','脚本' ,'音乐','播放电视台' ]
    count3=[]
    for x1 in x:
        count4=it(sorted(m[x1],key =lambda x:len(m[x1][x]))).map(lambda x:[x,len(m[x1][x]),m[x1][x]]).to_list()
        print(x1,count4[-3:])
        count3.append(count4[-3:])
    return count,count1,count2,count3

def check():
    print("角色的设定")
    print(len(character_data.keys()))
    result={}
    for i in character_data.keys():
        for y in character_data[i]['pos']:
            result[y]=result.get(y,0)+1
    for x,y in result.items():
        print(x,y)
    height=result['身高']
    weight=result['体重']
    print("地位有哪些")
    result={}
    for i in character_data.keys():
        y=character_data[i]['role']
        result[y]=result.get(y,0)+1
    for x,y in result.items():
        print(x,y)
    print("性别")
    result={}
    for i in character_data.keys():
        y=character_data[i]['pos'].get('性别',None)
        if y!=None:
            result[y]=result.get(y,0)+1
    for x,y in result.items():
        print(x,y)
    print()
    print("动漫作品的设定")
    result={}
    for i in cartoon_data.keys():
        if '放送星期'  in cartoon_data[i].keys():
            pass
            #print(cartoon_data[i]['放送开始'])
        for y in cartoon_data[i].keys():
            result[y] = result.get(y, 0) + 1
    for x,y in result.items():
        if y>10:
            print(x,y)
    print()
    print("ep")
    result = {}
    total=0
    for i in cartoon_data.keys():
        for z in cartoon_data[i]['ep']:
            for y in z.keys():
                result[y]=result.get(y,0)+1
            total+=1
            #print(z)
    for x,y in result.items():
            print(x,y)
    print(total)

    return height,weight
def get_norml_result():
    print('总动漫部数：',len(cartoon_rank1))
    print('总动漫部数(归类后)：' , len(cartoon_rank2))
    print("总动漫角色数:",len(character_data.keys()))
    print("总动漫角色数:",len(character_data.keys()))
    ch=sum(1 for x in character_data.keys() if character_data[x]['download']==True)
    print('有图片数：',ch)
    x=set()
    for i in cartoon_data.keys():
        for y in cartoon_data[i]['cv']:
            x.add(y['p_id'])
    print("总声优数:",len(x))
    pe=sum(1 for x in person_data.keys() if person_data[x]['download']==True)
    print('有图片数：',pe)
    return ch,pe
def get_character_rank(): #最高的身高/体重
    a=[]
    b=[]
    for key in character_data.keys() :
        height=character_data[key]['pos'].get("身高",None)
        weight=character_data[key]['pos'].get("体重",None)
        role=character_data[key].get("role",None)
        sex=character_data[key]['pos'].get("性别",None)
        if role=='主角' and height!=None:
            a.append([character_data[key]['name'],height,sex,key])
        if role=='主角' and weight!=None:
            b.append([character_data[key]['name'],weight,sex,key])
    def func(a,b,flag):
        a=it(a).filter(lambda x:x[2]==b).to_list()
        for x in range(len(a)):
            c = []
            for y in range(len(a[x][1])):
                if a[x][1][y] in (str(m) for m in range(10)):
                    c.append(a[x][1][y])
            #print(c)
            if c!=[]:
                if flag==0:
                    if int(c[0])!=1:
                        a[x][1]=None
                        continue
                    a[x][1]=int("".join(c[:3]))
                else:
                    if int(c[0]) ==1:
                        a[x][1]=int("".join(c[:3]))
                    else:
                        a[x][1]=int("".join(c[:2]))
            else:
                a[x][1]=None
        a=it(a).filter(lambda x: x[1]!=None).to_list()
        a=sorted(a,key=lambda x: x[1])
        print(a[0][0][0] if a[0][0][1]==None else a[0][0][1],a[0][1])
        print(a[-1][0][0] if a[-1][0][1]==None else a[-1][0][1],a[-1][1])
        return  [[a[0][0][0] if a[0][0][1]==None else a[0][0][1],a[0][1],a[0][-1]],[a[-1][0][0] if a[0][-1][1]==None else a[-1][0][1],a[-1][1],a[-1][-1]]]
    z=func(a,'男',0)
    x=func(a, '女', 0)
    c=func(b, '男', 1)
    v=func(b, '女', 1)
    return [z,x,c,v]
def get_person_rank():
    def func(sex,role):
        m=dict()
        for key in person_data.keys():
            for key1 in person_data[key]['ch']:
                if character_data[key1]['role']==role and character_data[key1]['pos'].get('性别',None)==sex:
                    if m.get(key,None)==None:
                        m[key]=[key1]
                    else:
                        m[key].append(key1)
        n=it(m).map(lambda x: [x,m[x]]).to_list()
        n=sorted(n,key=lambda x: len(x[1]))
        print(n[-1])
        return n[-1]
    return [func("男","主角"),
    func("男", "配角"),
    func("女", "主角"),
    func("女", "配角")]

def generate():
    def add_pic(docker, key, url, li):
        if docker[key]['download'] == True:
            path = init_menu + "save/save/images/" + url + str(key) + ".jpg"
            if not os.path.exists(path):
                src = init_menu + 'save/total_img/' + url + str(key) + '.jpg'
                tar = path
                shutil.copy(src, tar)
            li.append(
                r'''\includegraphics[width=0.2\textwidth]{images/''' + url + r'''PIC}'''.replace('PIC',                                                                                str(key) + ".jpg"))
        return li
    ANS=[]
    m={'主角':[],'配角':[],'客串':[]}
    for x in character_data.keys():
        if character_data[x]['download']==True:
            m[character_data[x]['role']].append(x)
    def add(role,number):
        main=m['role']
        random.shuffle(main)
        main1=main[:number]
        for x in main1:
            random.shuffle(main)
            tmp=main[:4]+[x]
            random.shuffle(tmp)
            tmp1=[]
            for x1 in range(len(tmp)):
                if character_data[tmp[x1]]['name'][1] != None:
                    name = character_data[tmp[x1]]['name'][1]
                else:
                    name = character_data[tmp[x1]]['name'][0]
                if tmp[x1]==x:
                    ANS.append(chr(ord('A')+x1))
                tmp1.append(chr(ord('A')+x1)+':'+ ' '+name+r'\\')
                tmp1=add_pic(character_data_total, tmp[x1],'character/', tmp)
                tmp1.append(r'\newline')
        return tmp1

    #15 主角 10 配角 5 客串 每个2分 60
    #10部作品 四个ep名字 每个3分 30
    #5部作品的OP+ED名 2分
    path = "simsun.ttc"
    if not os.path.exists(path):
        src = total_menu + "save/test/simsun.ttc"
        tar = path
        shutil.copy(src, tar)
    with open(init_menu+'save/test/test.tex','w',encoding='utf-8') as f:
        ANS.append('第一部分')
        m=overleaf.Main_Test_textex
        a=add('主角',15)+add('配角', 10)+ add('客串', 5)
        m.replace('te1st',"".join(a))
        b=[]
        for x in cartoon_data.keys():
            if len(cartoon_data[x]['ep'])>10:
                b.append(x)
        c=[]
        ANS.append('第三部分')
        for x in cartoon_data.keys():
            if '片头曲' in cartoon_data[x].keys() and '片尾曲' in cartoon_data[x].keys():
                c.append(x)
        for x in c:
            random.shuffle(c)
            tmp=c[:4]+[x]
            random.shuffle(c)
            tmp1=[]
            tmp1.append('片头曲:'+cartoon_data[x]['片头曲']+r'//'+'片尾曲'+cartoon_data[x]['片尾曲']+r'//')
            for x1 in range(len(tmp)):
                if tmp[x1]==x:
                    ANS.append(chr(ord('A')+x1))
                tmp1.append(chr(ord('A')+x1)+':'+ ' '+cartoon_data[tmp[x1]]['中文名']+r'\\')
        m.replace('te3st', "".join(c))
        f.write(m)
    print(ANS)

def draw():
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 宋体
    # 等价于：plt.rcParams['font.family']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    def bar(x_labels,y_values,rl):
        # 创建柱状图
        plt.figure(figsize=(8, 6))
        bars = plt.bar(x_labels, y_values, color='skyblue')

        # 在每个柱子上方显示数值
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, yval, ha='center', va='bottom')
        # 隐藏y轴
        plt.gca().axes.get_yaxis().set_visible(False)
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        # 保存为图片
        plt.savefig(rl, bbox_inches='tight')
        # 展示图片
    def plot(x_labels,y_values,rl):
        # 创建柱状图
        plt.figure(figsize=(8, 6))
        plot = plt.plot(x_labels, y_values, color='skyblue')
        plt.xticks(fontsize=10,rotation=45)
        # 保存为图片
        plt.savefig(rl, bbox_inches='tight')
        # 展示图片

    bar(list(x[0] for x in COUNT),list(x[1] for x in COUNT),init_menu+'save/overleaf/images/episode_count.png')
    x_labels=['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
    y_labels=[]
    for x in x_labels:
        for y in COUNT1:
            if y[0]==x:
                y_labels.append(y[1])
                break
    bar(x_labels, y_labels, init_menu + 'save/overleaf/images/Date.png')
    plot(list(x[0] for x in RESULT['TIME_POINT_TOTAL']),list(x[1] for x in RESULT['TIME_POINT_TOTAL']),init_menu+ 'save/overleaf/images/times.png')
    plot(list(x[0] for x in RESULT['TIME_POINT_TOTAL']), [0]+RESULT['UPDATE_TOTAL'],
         init_menu + 'save/overleaf/images/update_rate.png')

    MAX = max(list(x[0] for x in RESULT['ANI_DATE']) + list(x[1] for x in RESULT['ANI_DATE']))
    MIN = min(list(x[0] for x in RESULT['ANI_DATE']) + list(x[1] for x in RESULT['ANI_DATE']))
    x_labels =list(x1 for x1 in range(int(MIN+1),int(MAX-1),int(MAX-MIN)//50))
    y_labels=list(0 for x1 in range(len(x_labels)))
    max_1=result.I2D(MAX)
    max_1=int(max_1[:max_1.find("年")])
    min_1=result.I2D(MIN)
    min_1 = int(min_1[:min_1.find("年")])
    m=range(min_1,max_1,(max_1-min_1)//10)
    for x1 in RESULT['ANI_DATE']:
        for y1 in range(len(x_labels)):
            if x_labels[y1]<x1[1] and x_labels[y1]>x1[0]:
                y_labels[y1]+=1
    plt.figure(figsize=(8, 6))
    plot = plt.plot(x_labels, y_labels, color='skyblue')
    plt.xticks([result.D2I(str(x)+"年01月01日") for x in m],[str(x)+"年" for x in m])
    plt.xticks(fontsize=10, rotation=45)
    # 保存为图片
    plt.savefig(init_menu + 'save/overleaf/images/ani_date.png', bbox_inches='tight')
def latex_to_pdf(latex_file):
    # 获取文件的目录和名称（不包括扩展名）
    dir_name = os.path.dirname(latex_file)
    base_name = os.path.basename(latex_file).replace('.tex', '')
    # 调用xelatex命令
    result = subprocess.run(
        ['xelatex', '-interaction=nonstopmode', latex_file],
        cwd=dir_name,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # 检查生成的PDF是否存在
    pdf_file = os.path.join(dir_name, base_name + '.pdf')
    if os.path.exists(pdf_file):
        print(f"PDF generated successfully: {pdf_file}")
    else:
        print("PDF generation failed.")


to_csv()
a=result_1()
for x in a.keys():
    print(x,a[x])
RESULT=result_1()
COUNT,COUNT1,COUNT2,COUNT3=result_2()
COUNT2=list(COUNT2)
HEIGHT,WEIGHT=check()
CH,PE=get_norml_result()
CH_RA=get_character_rank()
PE_RA=get_person_rank()
draw()
tmp=list([x,cartoon_data[x]['中文名'],cartoon_data[x]['放送开始'],cartoon_data[x]['rank']] for x in cartoon_data.keys() if cartoon_data[x]['放送开始']!=None and cartoon_data[x]['rank']!='')
tmp1=sorted(tmp,key=lambda x:result.D2I(x[2]))
ANI1=tmp1[0]
ANI2=tmp1[-1]
tmp2=sorted(tmp,key=lambda x:int(x[3]))
ANI3=tmp2[0]
ANI4=tmp2[-1]
print(ANI1)
def main(user):
    path = "simsun.ttc"
    if not os.path.exists(path):
        src = total_menu + "save/simsun.ttc"
        tar = path
        shutil.copy(src, tar)
    with open(init_menu+'save/overleaf/main.tex','w',encoding='utf-8') as f:
        m=overleaf.Main_tex
        m=m.replace('USER',user)
        m=m.replace('LOOK_COUNT1',str(len(cartoon_rank2)))
        m=m.replace('LOOK_COUNT2',"".join(str(x) for x in RESULT['ANI_TIME_TOTAL']))
        m = m.replace('LOOK_COUNT3', str(len(cartoon_rank1)))
        m=m.replace('MEDIUM', RESULT['AVG_TIME'])
        m=m.replace('CH_COUNT',str(CH))
        m=m.replace('PE_COUNT',str(PE))
        m=m.replace('TIME',result.NOW())
        m = m.replace('AVG_UPDATE',str(int(RESULT['UPDATE_SUM']*1000)/10))
        f.write(m)
    with open(init_menu + 'save/overleaf/Chapters/Statistics.tex', 'w', encoding='utf-8') as f:
        def add_pic(key,li):
            path = init_menu + "save/overleaf/images/anime/" + str(key) + ".jpg"
            if not os.path.exists(path):
                    src = init_menu + 'save/total_img/'+ str(key) + '.jpg'
                    tar = path
                    shutil.copy(src, tar)
            li.append(r'''\includegraphics[width=0.25\textwidth]{images/anime/'''+r'''PIC}\newline'''.replace('PIC', str(key) + ".jpg"))
            return li
        m=overleaf.Statistics_tex
        m = m.replace('USER', user)
        st=[ANI1[1],' ',ANI1[2],r'\\\\']
        st=add_pic(ANI1[0], st)
        m = m.replace('ANI1', ''.join(st))
        st=[ANI2[1],' ',ANI2[2],r'\\\\']
        st=add_pic(ANI2[0], st)
        m = m.replace('ANI2', ''.join(st))
        st=[ANI3[1],' ',ANI3[3],r'\\\\']
        st=add_pic(ANI3[0], st)
        m = m.replace('ANI3', ''.join(st))
        st=[ANI4[1],' ',ANI4[3],r'\\\\']
        st=add_pic(ANI4[0], st)
        m = m.replace('ANI4', ''.join(st))
        f.write(m)
    with open(init_menu+'save/overleaf/Chapters/Staff.tex','w',encoding='utf-8') as f:
        def func(m, name, loc, name_1, loc_2):
            m = m.replace(name, COUNT3[loc_2][loc][0] + ' ' + str(COUNT3[loc_2][loc][1]) + '部')
            pic = []
            a = 0
            for x in COUNT3[loc_2][loc][2]:
                a += 1
                path = init_menu + "save/overleaf/images/anime/" + str(x) + ".jpg"
                if not os.path.exists(path):
                    src = init_menu + 'save/total_img/' + x + '.jpg'
                    tar = path
                    shutil.copy(src, tar)
                pic.append(r'''\includegraphics[width=0.125\textwidth]{images/anime/%s}''' % (str(x) + ".jpg"))
                if a % 4 == 0 and a != len(COUNT3[loc_2][loc][2]):
                    pic.append('\\newline')
            pic.append('\\newline')
            m = m.replace(name_1, ''.join(pic))
            return m
        m=overleaf.Staff_tex
        m = m.replace('USER', user)
        m = func(m,'JIAN1', -1, 'JIAPIC1',0)
        m = func(m, 'JIAN2', -2, 'JIAPIC2',0)
        m = func(m, 'JIAN3', -3, 'JIAPIC3',0)
        m = func(m, 'XI1', -1, 'XPIC1',1)
        m = func(m, 'XI2', -2, 'XPIC2', 1)
        m = func(m, 'XI3', -3, 'XPIC3', 1)
        m = func(m, 'RE1', -1, 'RPIC1', 2)
        m = func(m, 'RE2', -2, 'RPIC2', 2)
        m = func(m, 'RE3', -3, 'RPIC3', 2)
        m = func(m, 'JB1', -1, 'JPIC1', 3)
        m = func(m, 'JB2', -2, 'JPIC2', 3)
        m = func(m, 'JB3', -3, 'JPIC3', 3)
        m = func(m, 'YY1', -1, 'YPICY1', 4)
        m = func(m, 'YY2', -2, 'YPICY2', 4)
        m = func(m, 'YY3', -3, 'YPICY3', 4)
        m = m.replace('TV1', COUNT3[5][-1][0]+' '+str(COUNT3[5][-1][1])+'部')
        m = m.replace('TV2', COUNT3[5][-2][0] + ' ' + str(COUNT3[5][-2][1]) + '部')
        m = m.replace('TV3', COUNT3[5][-3][0] + ' ' + str(COUNT3[5][-3][1]) + '部')
        a=[]
        for x in range(len(COUNT2)):
            a.append(r'\\RANK%d： %s %d部\\\\'%(x,COUNT2[::-1][x][0],COUNT2[::-1][x][1]))
            for y in COUNT2[::-1][x][2]:
                a.append(r'%s\\'%cartoon_data[y]['中文名'])
        m = m.replace('PRODUCER',''.join(a))
        f.write(m)
    with open(init_menu+'save/overleaf/Chapters/Cv and Character.tex','w',encoding='utf-8') as f:
        m=overleaf.CvCharacter_tex
        def add_pic(docker,key,url,li):
            if docker[key]['download']==True:
                path = init_menu + "save/overleaf/images/"+url + str(key) + ".jpg"
                if not os.path.exists(path):
                    src = init_menu + 'save/total_img/'+url + str(key) + '.jpg'
                    tar = path
                    shutil.copy(src, tar)
                li.append(
                    r'''\includegraphics[width=0.1\textwidth]{images/'''+url+r'''PIC}'''.replace('PIC', str(key) + ".jpg"))
            return li
        def PE_R(x):
            a=[]
            m=PE_RA[x]
            m1=person_data[m[0]]['name']
            if m1[1]!="":
                m1=m1[1]
            else:
                m1=m1[0]
            a.append(m1+' '+'%d名'%len(m[1])+r'\\')
            a=add_pic(person_data, m[0], 'person/',a)

            a.append(r'\newline 分别是')
            a_2=[]
            els=[]#存语句
            els1=[] #存角色地址
            for x in person_data[m[0]]['src']:
                flg=False
                if x in cartoon_data.keys():
                    tmp=[r'来自%s的 '%cartoon_data[x]['中文名']]
                    for x1 in m[1]:
                        if x==character_data[x1]['src']:
                            name=character_data[x1]['name']
                            if name[1] != None:
                                name = name[1]
                            else:
                                name = name[0]
                            tmp.append(r'%s\\'%name)
                            a_2.append(x1)
                            flg=True
                    if flg:
                        tmp.append(r'\\')
                        a=a+tmp
                    else:#除了当前角色外担任的别的角色
                        for x1 in person_data[m[0]]['ch']:
                            if x == character_data[x1]['src']:
                                name = character_data[x1]['name']
                                if name[1] != None and name[1] != "" :
                                    name = name[1]
                                else:
                                    name = name[0]
                                tmp.append(r'%s %s\\' % (character_data[x1]['role'],name))
                                els1.append(x1)
                                flg=True
                        if flg:
                            tmp.append(r'\\')
                            els+=tmp
            a.append(r'\\')

            count = 0
            for x in a_2:
                count += 1
                a = add_pic(character_data, x, 'character/', a)
                if count % 4 == 0 and count != len(a_2):
                    a.append(r'\newline')
            a.append(r'\newline')
            a.append(r'   除此之外还有\\')
            for x in els:
                a+=x
            a.append(r'\\')
            count = 0
            for x in els1:
                count += 1
                a = add_pic(character_data, x, 'character/', a)
                if count % 4 == 0 and count != len(els1):
                    a.append(r'\newline')
            a.append(r'\newline')

            return a

        m = m.replace('CV1', "".join(PE_R(0)))
        m = m.replace('CV2', "".join(PE_R(1)))
        m = m.replace('CV3', "".join(PE_R(2)))
        m = m.replace('CV4', "".join(PE_R(3)))
        m = m.replace('CH1', str(CH))
        m = m.replace('CH2',str(HEIGHT))
        m = m.replace('CH3', str(WEIGHT))
        def func2(ar1,ar2,name,tag,m):
            a = [CH_RA[ar1][ar2][0], " ", CH_RA[ar1][ar2][1], tag, r"\newline"]
            a = add_pic(character_data, CH_RA[ar1][ar2][2], 'character/', a)
            a.append(r'\newline')
            m = m.replace(name, "".join(str(x)for x in a))
            return m
        m = func2(0, 0, 'CH_M_1','CM', m)
        m = func2(0, 1, 'CH_M_2', 'CM', m)
        m = func2(1, 0, 'CH_F_1', 'CM', m)
        m = func2(1, 1, 'CH_F_2', 'CM', m)
        m = func2(2, 0, 'CH_M_3', 'KG', m)
        m = func2(2, 1, 'CH_M_4', 'KG', m)
        m = func2(3, 0, 'CH_F_3', 'KG', m)
        m = func2(3, 1, 'CH_F_4', 'KG', m)



        f.write(m)
    with open(init_menu + 'save/overleaf/Chapters/Potential Future Directions.tex', 'w', encoding='utf-8') as f:
        m=overleaf.Potential_Future_Directions_tex
        f.write(m)

main('薛定谔的猫')

    # USER看番数为 LOOK_COUNT1（系列作合并）\\
    # USER等效总计看番部数为 LOOK_COUNT2\\
    # USER所看番剧所发布时间中位数为 MEDIUM\\
    # 本次爬取动漫角色声优数： CH_COUNT\\声优数：PE_COUNT\\
#generate()