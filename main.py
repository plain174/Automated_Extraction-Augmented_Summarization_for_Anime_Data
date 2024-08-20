import pandas as pd
import json
import time
from 爬虫 import get_save,get_url,down_pic,down_pic_usual,fix_name,find_bangumi
from create_ico import reset
import os
import shutil

#等以后把电影做进来了把电影单独划出去
#不知道bangumi能不能搜小说和音乐
#找找原声集
#浓度检测器 随机声优和角色图片 随机集的名字

cartoon_data_total=dict()#把不同分目录的数据都存在一个地方。明智的选择
person_data_total=dict()
character_data_total=dict()

total_total_data=[cartoon_data_total,person_data_total,character_data_total]
#json读取出来字典的键只能是字符串。烂。总之除了cartoon_list值是整数外把其他字典键都改成字符串了
#json集合也存不了
cartoon_list=dict()#excel读取存储表

cartoon_data=dict()#爬虫爬下来的 蛮多的自己看
person_data=dict()#id:{'img':图片地址,'name':名字,'download':False,'src':{id},ch:[]} #这边src存的是角色的信息？
character_data=dict()#id:{'img':c_img,'name':c_name,'role':地位,'pos':各种属性,'download':False,'src':id}
total_data=[cartoon_data,person_data,character_data]
cartoon_rank1=[]#按观看顺序来排名
cartoon_rank2=[]#按排名来排序,合并了同一个的
cartoon_rank3=[]
#init_menu="C:/Users/17402/Desktop/爬虫/"#输出不同目录 可更改部分
init_menu="C:/Users/17402/Desktop/爬虫/new/"
#total_menu="C:/Users/17402/Desktop/爬虫/"
total_menu="C:/Users/17402/Desktop/爬虫/total/"
excel_url="C:/Users/17402/Desktop/爬虫/new/番剧记录平野.csv"
def open_excel(excel_url):#打开excel
    global cartoon_rank1,cartoon_rank2,cartoon_rank3
    cartoon_rank1=[]
    cartoon_rank2=[]
    cartoon_rank3=[]
    excel_url=open(excel_url)
    a=pd.read_csv(excel_url)
    a.loc[a.isnull().排名 == True, '排名'] = 0
    a.loc[a.isnull().季数 == True, '季数'] = 1
    a_drop=a[a.isnull().bangumi==False].reset_index(drop=True)
    for x in a.index:
        if a.isnull()[a.index==x].bangumi.item()==True:
            cartoon_rank3.append(a[a.index==x].名字.item()) ##rank3用于result.py
        else:
            m=a[a.index==x]
            cartoon_rank3.append([int(m.排名.item()),int(m.季数.item()),m.名字.item(),int(m.bangumi.item())])
    a_drop.loc[a_drop.isnull().注释 == True,'注释']=None
    for i in range(len(a_drop)):
        b=a_drop[a_drop.index==i]
        #print(type(b.bangumi.item()))
        cartoon_rank1.append(int(b.bangumi.item()))
        if b.排名.item()!=0:
            try:
                if cartoon_list.get(int(b.bangumi.item()))!=None:
                    print(b.名字.item())
                    return False
                cartoon_list[int(b.bangumi.item())]=[int(b.排名.item()),int(b.季数.item()),b.名字.item(),b.注释.item(),int(b.index.item())]
                cartoon_rank2.append([int(b.bangumi.item())])
            except :
                print(b)
        else:
                for x in range(len(cartoon_rank2)):
                    if(b.名字.item()==cartoon_list[cartoon_rank2[x][0]][2]):
                        cartoon_rank2[x].append(int(b.bangumi.item()))
                        cartoon_list[int(b.bangumi.item())] = [
                            cartoon_list[cartoon_rank2[x][0]][0], int(b.季数.item()), b.名字.item(), b.注释.item(), int(b.index.item()),
                             ]
                        break
                else:
                    print(b)
                    print('输入表格有误')
                    #sys.exit()

    excel_url.close()
    return True
def isexist_data():#补充数据库内容
    for x in cartoon_list.keys():
        x=str(x)
        if x not in cartoon_data_total.keys():
            print(x)
            content = get_url('https://bangumi.tv/subject/' + x)
            time.sleep(1)
            content1 = get_url('https://bangumi.tv/subject/' + x + '/characters')
            save_dict = get_save(content, content1, x,person_data_total,character_data_total)
            cartoon_data_total[x] = save_dict
            if not os.path.exists(init_menu + "save/total_img/" + x + '.jpg'):
                time.sleep(1)
                down_pic(content, init_menu + "save/total_img/" + x + '.jpg')
            time.sleep(2)


def isexist_data2(): #补充肖像类文件
    for x in person_data.keys():
        if person_data_total[x]['download']==False and person_data_total[x]['img']!=None:
            if down_pic_usual(person_data_total[x]['img'],total_menu+'save/total_img/person/'+str(x)+'.jpg')==False:
                person_data_total[x]['img']=None
                continue
            person_data_total[x]['download'] = True
            #time.sleep(0.5)
    print('perpson载入完成')
    for x in character_data.keys():
        if character_data_total[x]['download']==False and character_data_total[x]['img']!=None:
            if down_pic_usual(character_data_total[x]['img'],total_menu+'save/total_img/character/'+str(x)+'.jpg')==False:
                character_data_total[x]['img']=None
                continue
            character_data_total[x]['download'] = True
            #time.sleep(0.5)

def copy():
    for x in cartoon_list.keys():
        x=str(x)
        for dic in cartoon_data_total[x]['cv']:
            person_data[dic['p_id']]=person_data_total[dic['p_id']]
            if person_data_total[dic['p_id']]['img'] != None:
                src = total_menu + 'save/total_img/person/' + str(dic['p_id']) + '.jpg'
                tar = init_menu + 'save/total_img/person/' + str(dic['p_id']) + '.jpg'
                shutil.copy(src, tar)
            character_data[dic['c_id']] = character_data_total[dic['c_id']]
            if character_data_total[dic['c_id']]['img'] != None:
                src = total_menu + 'save/total_img/character/' + str(dic['c_id']) + '.jpg'
                tar = init_menu + 'save/total_img/character/' + str(dic['c_id']) + '.jpg'
                shutil.copy(src, tar)

    for x in cartoon_list.keys():
        x=str(x)
        if x not in cartoon_data.keys():
            cartoon_data[x] = cartoon_data_total[x]
            src = total_menu + 'save/total_img/' + str(x) + '.jpg'
            tar = init_menu + 'save/total_img/' + str(x) + '.jpg'
            shutil.copy(src, tar)
def check_isexist_update_ch_and_pe():
    def Multiplexing(person_data,url):#设定为true但文件很小，重新下载空文件
        for x in person_data.keys():
            if person_data[x]['download'] == True:
                rl = total_menu + 'save/total_img/'+url+'/' + str(x) + '.jpg'
                if os.path.exists(rl):
                    if os.stat(rl).st_size <= 512:
                        print(x)
                        try:
                            if down_pic_usual(person_data[x]['img'],rl) !=True:
                                person_data[x]['download'] = False
                                person_data[x]['img'] = None
                        except:
                            person_data[x]['download'] = False
                else:
                    person_data[x]['download'] = False

    Multiplexing(person_data_total,'person')
    Multiplexing(character_data_total, 'character')
def check_isexist_update_ch_and_pe2():#补一下设定 文件大于大小则把设定补充为true
    def Multiplexing(person_data,url):
        for x in person_data.keys():
                rl = total_menu + 'save/total_img/'+url+'/' + str(x) + '.jpg'
                if os.path.exists(rl):
                    if os.stat(rl).st_size >= 512:
                        person_data[x]['download'] = True
    Multiplexing(person_data_total,'person')
    Multiplexing(character_data_total, 'character')
def isexist_content():#填充目录内容
    con=init_menu+"save/anime/"
    alist=os.listdir(con)
    len_al=len(alist)
    for x in range(len(cartoon_rank2)):
        name=cartoon_data[str(cartoon_rank2[x][0])]['中文名']
        name_rl=str(x+1)+"."+name
        if name_rl not in alist:#判断原有在不在，不在就开删然后建
            os.mkdir(con+name_rl)
            if x<len_al:#删除有变更的内容
                for co in  os.listdir(con+alist[x]):
                    if os.path.isdir(con+alist[x]+"/"+co):
                        for co1 in os.listdir(con+alist[x]+"/"+co):
                            os.remove(con+alist[x]+"/"+co+'/'+co1)
                    else:
                        os.remove(con+alist[x]+"/"+co)
                os.remove(con+alist[x])
            if len(cartoon_rank2[x])==1:#添加图片
                pass
            else:
                for y in cartoon_rank2[x]:
                    y=str(y)
                    os.mkdir(con+name_rl+'/'+cartoon_data[y]['中文名'])
                    src=init_menu+'save/total_img/' + y + '.jpg'
                    tar=con+name_rl+'/'+cartoon_data[y]['中文名']+'/'+y+'.jpg'
                    shutil.copy(src,tar)
            src = init_menu + 'save/total_img/' + str(cartoon_rank2[x][0]) + '.jpg'
            tar = con + name_rl + '/' + str(cartoon_rank2[x][0]) + '.jpg'
            shutil.copy(src, tar)
    reset(con)
def data_strip():
    for x in cartoon_data_total.keys():
        for y in cartoon_data_total[x].keys():
                if type(cartoon_data_total[x][y])==type('1'):
                    cartoon_data_total[x][y]=cartoon_data_total[x][y].strip()
def cover_none():
    for x in cartoon_data_total.keys():
        if '播放结束' not in x:
            add_time=time.mktime(time.strptime(cartoon_data_total[x]['放送开始'],"%Y年%m月%d日"))+60*60*24*7*int(cartoon_data_total[x]['话数'])
            cartoon_data_total[x]['播放结束']=time.strftime("%Y年%m月%d日",time.localtime(add_time))
            #print(cartoon_data[x]['放送开始'])
            #print(cartoon_data[x]['播放结束'])
def add_person(): #之前写代码不完善用的补充技巧 实际上也不完善，这个函数根本用不了
    for x in person_data:
        person_data[x]['ch'] = 0
    for x in cartoon_data.keys():
        for y in cartoon_data[x]['cv']:
            if person_data[y[3]]['ch'] == 0:
                person_data[y[3]]['ch'] = [y[2]]
            else:
                person_data[y[3]]['ch'].append(y[2])
    for x in person_data.keys():
        person_data[x]['ch'] = list(set(person_data[x]['ch']))
def isexist_index():#没有目录就创建
    def func(init_menu):
        if "save" not in os.listdir(init_menu):
            os.mkdir(init_menu + "save")
        if "total_img" not in os.listdir(init_menu + "save"):
            os.mkdir(init_menu + "save/total_img")
        if "person" not in os.listdir(init_menu + "save/total_img"):
            os.mkdir(init_menu + "save/total_img/person")
        if "character" not in os.listdir(init_menu + "save/total_img"):
            os.mkdir(init_menu + "save/total_img/character")
    func(init_menu)
    func(total_menu)
    if "anime" not in os.listdir(init_menu + "save"):
        os.mkdir(init_menu + "save/anime")
    if "overleaf" not in os.listdir(init_menu+"save"):
        os.mkdir(init_menu+"save/overleaf")
    if "Chapters" not in os.listdir(init_menu+"save/overleaf"):
        os.mkdir(init_menu+"save/overleaf/Chapters")
    if "images" not in os.listdir(init_menu+"save/overleaf"):
        os.mkdir(init_menu+"save/overleaf/images")
    if "anime" not in os.listdir(init_menu+"save/overleaf/images"):
        os.mkdir(init_menu+"save/overleaf/images/anime")
    if "person" not in os.listdir(init_menu+"save/overleaf/images"):
        os.mkdir(init_menu+"save/overleaf/images/person")
    if "character" not in os.listdir(init_menu+"save/overleaf/images"):
        os.mkdir(init_menu+"save/overleaf/images/character")

def upload_json_init():
    global cartoon_rank1,cartoon_rank2,cartoon_data,person_data,character_data
    with open(init_menu+"save/struct.json","r") as m:
        try:
            save_json=json.load(m)
            cartoon_rank1,cartoon_rank2,cartoon_rank3=save_json
        except :
            pass
    with open(init_menu+"save/data.json","r") as m:
        try:
            save_json=json.load(m)
            total_data=save_json
            cartoon_data,person_data,character_data=total_data
        except Exception as e:
            print("传入失败"+e)

def upload_json():
    global cartoon_data_total,person_data_total,character_data_total
    with open(total_menu+"save/data.json","r") as m:
        try:
            save_json=json.load(m)
            total_data_total=save_json
            cartoon_data_total,person_data_total,character_data_total=total_data_total
        except Exception as e:
            print("源数据传入失败"+e)

def load_json_init():#将已经有的数据存进去
    with open(init_menu+"save/struct.json","w") as m:
        json.dump([cartoon_rank1,cartoon_rank2,cartoon_rank3],m)
    with open(init_menu+"save/data.json","w") as m:
        total_data = [cartoon_data, person_data, character_data]
        json.dump(total_data,m)
def load_json():#将已经有的数据存进去
    with open(total_menu+"save/data.json","w") as m:
        total_data_total = [cartoon_data_total,person_data_total,character_data_total]
        json.dump(total_data_total,m)

def Max():
    return len(cartoon_rank1)
def read_e(pri=False):#读入excel并进行初始化
    if pri:
        upload_json()
    if open_excel(excel_url)==False:
        print("读取失败")
        return
    isexist_index()
    try:
        isexist_data()
        print("载入数据完成")
    except Exception as e:
        load_json()
        print("失败原因"+str(e))
        return
    data_strip()#清理数据
    cover_none()#填充不存在数据
    fix_name(cartoon_data_total) #看看有没有不存在的中文名，没有则补充
    print('修补完成')
    load_json() #存入源数据
    isexist_data2()
    #check_isexist_update_ch_and_pe2()
    #check_isexist_update_ch_and_pe()
    load_json()
    copy()#复制一份数据
    load_json_init()
    print('开始创建目录')
    isexist_content()
'''upload_json()
for keys in cartoon_data_total.keys():
    m=cartoon_data_total[keys]['cv']
    cartoon_data_total[keys]['cv']=list(it(m).map(lambda x: {"p_id":x[3],"c_id":x[2]}))
load_json()'''
#read_e(True)
#print(cartoon_data_total['316247'])
#cartoon_data_total1=dict()#把不同分目录的数据都存在一个地方。明智的选择
#person_data_total1=dict()
#character_data_total1=dict()
#with open('C:/Users/17402/Desktop/爬虫/' + "save/data.json", "w") as m:
#    total_data_total1 = [cartoon_data_total1, person_data_total1, character_data_total1]
#    json.dump(total_data_total1, m)
#print(cartoon_data_total1['316247'])