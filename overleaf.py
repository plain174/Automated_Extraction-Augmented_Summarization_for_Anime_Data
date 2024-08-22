Main_tex=r'''
\documentclass[lettersize,journal,article,UniThesis]{IEEEtran}
\usepackage{ctex}
\setCJKmainfont{SIMSUN.TTC}
\usepackage{graphicx}


\begin{document}

\title{Automated Extraction-Augmented Summarization for Anime Data: An Attempt}

\author{Author: Plain User: USER \\TIME var 1.0 }

\maketitle
\begin{center}
\textbf{\Large Abstract}
\end{center}
本项目旨在为用户提供看番总结。我使用Python爬虫[1]爬取了Bangumi网站[2]的相关数据，在试运行时使用Overleaf[3]调试，最后使用Tex Live[4]进行标记文本转pdf的过程。详细引用请参见文末的网址。
\begin{itemize}
    \item 用户共观看LOOK_COUNT1部番剧（系列作合并计数）。
    \item 累计观看番剧总数为LOOK_COUNT3部，涵盖动漫角色CH_COUNT名,涉及声优PE_COUNT名。
    \item 用户的平均追番率为AVG_UPDATE%
    \item 按标准时间（十二集二十四分钟）等效看番部数为LOOK_COUNT2。
    \item 所看番剧的发布时间中位数为MEDIUM。
\end{itemize}
\input{Chapters/Statistics}
\input{Chapters/Staff}
\input{Chapters/Cv and Character}
\input{Chapters/Potential Future Directions}

\vfill

\end{document}

'''
#TIME
#USER看番数为 LOOK_COUNT1（系列作合并）\\
#USER等效总计看番部数为 LOOK_COUNT2\\
#USER所看番剧所发布时间中位数为 MEDIUM\\
#本次爬取动漫角色声优数： CH_COUNT\\声优数：PE_COUNT\\
Statistics_tex=r'''\section{Statistics}

This study presents a detailed analysis of anime viewing habits among users, as well as the broadcast characteristics of anime series over specific periods. The data is visualized in five distinct figures, each offering unique insights into the dynamics of anime consumption and distribution.
\includegraphics[width=0.4\textwidth]{images/times.png}
\newline
Fig. 1 用户每季度看番数量折线图
\newline
\includegraphics[width=0.5\textwidth]{images/update_rate.png}
\newline
Fig. 2 用户每季度追番率折线图
\newline
\includegraphics[width=0.5\textwidth]{images/Date.png}
\newline
Fig. 3 番剧播出时间统计折线图
\newline
\includegraphics[width=0.5\textwidth]{images/ani_date.png}
\newline
Fig. 4 番剧播出时间段统计折线图
\newline
\includegraphics[width=0.5\textwidth]{images/episode_count.png}
\newline
Fig. 5 番剧集数统计柱状图\\\\
播出日期最近的番剧：  ANI2
播出日期最久远的番剧：  ANI1 
bangumi上排名最高的番剧：  ANI3
bangumi上排名最低的番剧：  ANI4

'''
Staff_tex=r'''

\section{Staff}
在USER所看番剧中频繁出现的staff:\\
\textbf{监督：}\\
RANK1： JIAN1\\\\
JIAPIC1
RANK2： JIAN2\\\\
JIAPIC2
RANK3： JIAN3\\\\
JIAPIC3
\textbf{系列构成：}\\\\
RANK1： XI1\\\\
XPIC1
RANK2： XI2\\\\
XPIC2
RANK3： XI3\\\\
XPIC3
\textbf{人物设定：}\\\\
RANK1： RE1\\\\
RPIC1
RANK2： RE2\\\\
RPIC2
RANK3： RE3\\\\
RPIC3
\textbf{脚本：}\\\\
RANK1： JB1\\\\
JPIC1
RANK2： JB2\\\\
JPIC2
RANK3： JB3\\\\
JPIC3
\textbf{音乐：}\\\\
RANK1： YY1\\\\
YPICY1
RANK2： YY2\\\\
YPICY2
RANK3： YY3\\\\
YPICY3
\textbf{播放电视台：}\\\\
RANK1： TV1\\
RANK2： TV2\\
RANK3： TV3\\\newline
\textbf{制作社：}\\
PRODUCER\\

'''
CvCharacter_tex=r'''\section{Cv And Character}
担任最多男主角的CV为CV1 \\
担任最多男配角的CV为CV2 \\
担任最多女主角的CV为CV3 \\
担任最多女配角的CV为CV4 \\

在共CH1名角色中，
爬取了CH2个身高数据，\\
其中身高最矮的男性为 CH_M_1
身高最高的男性为 CH_M_2
身高最矮的女性为 CH_F_1
身高最高的女性为 CH_F_2
爬取了CH3个体重数据\\
其中体重最轻的男性为 CH_M_3
其中体重最重的男性为 CH_M_4
其中体重最轻的女性为 CH_F_3
其中体重最重的女性为 CH_F_4
'''
Potential_Future_Directions_tex=r'''
\section{Potential Future Directions}
以下按实现难度和实现迫切性排列
\begin{itemize}
    \item   自动爬取动漫原声集
    \item   管理用户写的动漫评论
    \item √ 引入模糊搜索，利用用户给的名字自动获得bangumi号
    \item   引入更强大的动漫tag系统进行tag分析
    \item   爬取更多关于角色的信息。在P站爬取主角的图片。
    \item   对于爬取的无结构文本使用AI进行解析利用
    \item   制作网站
    \item   制作图形化界面，让普通用户能轻松过使用
\end{itemize}
本次更新内容：引入模糊搜索，利用用户给的名字自动获得bangumi号
\begin{center}
\textbf{\Large ltimation}
\end{center}
\begin{itemize}
\item 搜索出的bangumi号生成excel数据处理中会有不知名bug
\end{itemize}
\begin{center}
\textbf{\Large Reference}
\end{center}
[1]python是一种解释型编程语言，有对于新手很友好的学习难度和应对各种情况的数量繁多的库。爬虫指用代码模仿人类访问网站以获得大量数据。 网址https://www.python.org/ 

[2]Bangumi是一家兼具维基和论坛性质的ACG网站，2008年7月由Sai在高考暑假的时候[参 1]创立，运营至今。截至2022年5月25日，共有374,654个维基条目被创建。
我不常用这个网址，但是它确实数据比较全，我也想过用萌娘百科，后来回忆起我有好几次连都连不上去就放弃了。网址https://bangumi.tv/ 

[3]Overleaf仅仅是一个LaTeX的在线解释器。LaTex格式跟HTML格式一样，用一部分命令和规范代替了所见即所得的编辑，但是用在代码生成文本方面很方便。
我在爬取数据后需要一个方便的输出，仅仅输出一个word文档就太丑了，但是以图片格式输出的话编译又会很麻烦。所以我选择了标记语言自动转换成PDF来输出。网址https://www.overleaf.com/project

[4]Tex Live 测试指令: tex --version 生成pdf指令: xelatex tex.tex --interaction=nonstopmode  官网网址https://tug.org/texlive/安装的网址镜像站https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/
'''

Test_tex=r'''
\documentclass[lettersize,journal,article,UniThesis]{IEEEtran}
\usepackage{ctex}
\setCJKmainfont{SIMSUN.TTC}
\usepackage{graphicx}


\begin{document}

\title{Test}

\author{满分：100分}

\maketitle
\begin{center}
\textbf{\Large 看图识人(60分)}
\end{center}
每题两分\\
te1st
\maketitle
\begin{center}
\textbf{\Large 看集名识片(30分)}
\end{center}
每题三分\\
te2st
\maketitle
\begin{center}
\textbf{\Large 看OP和ED名字识片(10分)}
\end{center}
每题两分\\
te3st
\vfill

\end{document}

'''