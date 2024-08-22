import urllib.request
from pyiter import it
from bs4 import BeautifulSoup
import ssl
import os
import time
ssl._create_default_https_context = ssl._create_unverified_context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

headers={U'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
         'Connection':'close'}
##记得json读出来后字典值会变成str

url='https://bangumi.tv/subject/415779/characters'
'''
with open('save.txt',encoding='utf-8') as m:
    m=m.read()
with open('save2.txt',encoding='utf-8') as n:
    n=n.read()
'''

def find_bangumi(url):
    soup=get_url('https://bangumi.tv/subject_search/%s?cat=2'%url)
    soup=BeautifulSoup(soup, "html.parser", from_encoding="utf-8")
    a=soup.body.div.contents[7].contents[1].contents[3].contents[3].contents[0].h3.a['href']
    return a[9:]
def find_all(n,m):
    a=[n.find(m)]
    while(n.find(m,a[-1]+1)!=-1):
        a.append(n.find(m,a[-1]+1))
    for x in range(len(a)):
        a[x]-=1
    return a
def get_url(url):
    try:
        request = urllib.request.Request(url, headers=headers)
        m=urllib.request.urlopen(request,timeout=5).read().decode('utf-8')
        if m==None or m=='\xa0':
            print("爬取为None")
            return get_url(url)
        return m
    except Exception as e:
        print(e)
        return get_url(url)

def fix_name(cartoon_data):
    for x in cartoon_data.keys():
        if '中文名' in cartoon_data[x].keys():
            cartoon_data[x]['中文名']=cartoon_data[x]['中文名'].strip()
        else:
            print('https://bangumi.tv/subject/' + x)
            content = get_url('https://bangumi.tv/subject/' + x)
            soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
            cartoon_data[x]['中文名']=soup.find_all('meta')[2]['content'].split(",")[0]
            print(cartoon_data[x]['中文名'])
            time.sleep(0.5)
def down_pic(m,n):#m为网址解析，n为图片存储地址
    try:
        for x in m.split('\n'):
            if 'width' in x and 'jpg' in x:
                x=x.split("\"")# 1和9都是，但是9糊
                if not os.path.exists(n):
                    with open(n,"wb") as f:
                        #print(x[1],x[9])
                        request = urllib.request.Request("http:"+x[1],headers=headers)
                        f.write(urllib.request.urlopen(request,timeout=5).read())
    except:
        down_pic(m, n)
def down_pic_usual(m,n):
    with open(n, "wb") as f:
        try:
            request = urllib.request.Request("http:" + m, headers=headers)
            f.write(urllib.request.urlopen(request, timeout=5).read())
        except urllib.error.HTTPError:
            print(m)
            return False
        except  Exception as e:
            print(e)
            down_pic_usual(m,n)
        return True
def get_save(m,n,id,person_data_total,character_data_total):#m为本体,n=m+'/characters'
    ep=[]
    tag={}
    for x in m.split('\n'):
        if("Bangumi Anime Ranked"in x):
            rank= "".join(x1 for x1 in x if x1 in it(range(10)).map(lambda x:str(x)))
        elif 'inner'in x and 'small' in x:
            X1=BeautifulSoup(x,features="html.parser")
            a=X1.find_all("span")#<span>恋爱</span>
            b=X1.find_all("small")#<small class="grey">496</small>
            for x1 in range(len(a)):
                try:
                    tag[a[x1].get_text()]=int(b[x1].get_text())
                except:
                    pass
    name_2=[]
    for x in n.split('\n'):
        if("a href=\"/person" in x and '<p>' in x):
            #print(x)
            name_2.append(x[x.find("class=\"grey\""):x.find("</small></p>")+1][x.find(">")-1:][:-1])
    soup = BeautifulSoup(m,"html.parser",from_encoding="utf-8")
    links = soup.find_all('li')
    save_dict=dict()
    for link in links: #提取制作人员表
        m=link.get_text()
        if ':' in m and 'CV' not in m:
            save_dict[m.split(':')[0]]=m.split(':')[1].strip()#
        if '片头曲' in m:
            save_dict['片头曲'] = m[6:-1]
        if '片尾曲' in m:
            save_dict['片尾曲'] = m[6:-1]
        if '原声集' in m:
            save_dict['原声集'] = m
    if '中文名' not in save_dict.keys():
        save_dict['中文名']=soup.find_all('meta')[2]['content'].split(",")[0].strip()
#中文名', '话数', '放送开始', '放送星期', '原作', '导演', '脚本', '分镜', '演出', '音乐', '人物设定', '系列构成', '美术监督', '色彩设计', '总作画监督', '作画监督', '道具设计', '原画', '第二原画', '背景美术', '剪辑', '主题歌编曲', '主题歌作曲', '主题歌作词', '主题歌演出', '企画', '录音', '製作', '音响监督', '音响', '音效', '执行制片人', '制片人', '音乐制作', '动画制作', 'OP・ED 分镜', '总导演', '制作协力', '动画制片人', '别名', '官方网站', '播放电视台', '其他电视台', '播放结束', 'Copyright', '摄影监督', '原声集',
    extract=soup.body.div.contents[7].contents[0].contents[3].contents[1].contents[1].contents[1].contents[15].contents
    extract1 = soup.body.div.contents[7].contents[0].contents[3].contents[1].contents[1].contents[1].contents[7].get_text().split()
    for x in range(len(extract)):
        x4 = dict()
        x2 = extract[x].contents[0].contents
        for x3 in x2:
            if ':' in x3:
                x4[x3.split(':')[0]] = ":".join(x3.split(':')[1:])
#这边记得加具体变量名
        ep.append(x4)

    soup1=BeautifulSoup(n,"html.parser",from_encoding="utf-8")
    extract=soup1.body.div.contents[7].contents[0].contents[1].contents
    extract=[extract[x] for x in range(len(extract)) if x%3==2]
    name_total=[]
    for z in extract:
        try:#比较冒失的决定
            c_img=z.contents[1].img['src']
            c_id=z.contents[1]['href'][11:]#id
            c_name=z.contents[5].contents[1].contents  # 0本名1中文名
            c_role=z.contents[5].contents[3].contents[1].get_text()#role
            c_dict=z.contents[5].contents[3].contents[3].contents#第一个舍去 字典
            p_img=z.contents[5].contents[5].img['src']
            p_id=z.contents[5].contents[5].a['href'][8:]
            p_name=z.contents[5].contents[5].p.contents  # 0 是代号1是本名
            if len(c_name)==2:
                c_name=[c_name[0].get_text(),None]
            else:
                c_name=[c_name[0].get_text(),c_name[2].get_text()[3:]]
            if len(p_name)==2:
                p_name=[p_name[0].get_text(),p_name[1].get_text()]
        except Exception as e:
            continue
        if c_id not in character_data_total.keys():
            character_data_total[c_id]={'img':c_img,'name':c_name,'role':c_role,'pos':dict(),'download':False,'src':id}
            for x in range(1,len(c_dict),2):
                character_data_total[c_id]['pos'][c_dict[x].get_text()]=c_dict[x+1].split()[0]

        if p_id not in person_data_total.keys():
            person_data_total[p_id]={'img':p_img,'name':p_name,'download':False,'src':[id],'ch':[c_id]}
        else:
            person_data_total[p_id]['src'].append(id)
            person_data_total[p_id]['ch'].append(c_id)
            person_data_total[p_id]['src']=list(set(person_data_total[p_id]['src']))
            person_data_total[p_id]['ch'] = list(set(person_data_total[p_id]['ch']))

        name_total.append({'c_id':c_id,'p_id':p_id})

    save_dict['ep']=ep  #
    save_dict['tag']=tag
    save_dict['rank']=rank
    save_dict['cv']=name_total
    return save_dict
