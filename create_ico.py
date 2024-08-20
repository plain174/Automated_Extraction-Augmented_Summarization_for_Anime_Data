import os
import subprocess
import codecs
import win32con
import win32api

ini_str = '''
[.ShellClassInfo]\r\n
IconResource=icon.ico,0\r\n
[ViewState]\r\n
Mode=\r\n
Vid=\r\n
FolderType=Pictures\r\n
'''

Any2Ico_path = 'Quick_Any2Ico.exe'
ext = ["jpg", "jpeg", "png", "gif", "icns", "ico"]

# 检查 Quick_Any2Ico.exe 是否存在
if not os.path.exists(Any2Ico_path):
    raise FileNotFoundError(f"The file {Any2Ico_path} does not exist. Please check the path.")

def reset(root):
    if root.upper() == 'Q':
        return
    root = root.strip('"').strip("'")
    print('--->', root)

    for parent, dirnames, filenames in os.walk(root):
        try:
                first = min(p for p in os.listdir(parent) if p.split(".")[-1].lower() in ext)
                cmd = f'"{Any2Ico_path}" "-img={parent}\\{first}" "-icon={parent}\\icon.ico"'
                subprocess.run(cmd, check=True)  # check=True 可以确保 subprocess 运行成功

                win32api.SetFileAttributes(f'{parent}/icon.ico', win32con.FILE_ATTRIBUTE_HIDDEN)

                desktop_ini = f'{parent}/desktop.ini'
                if os.path.exists(desktop_ini):
                    os.remove(desktop_ini)
                with codecs.open(desktop_ini, 'w', 'utf-8') as f:
                    f.write(ini_str)
                win32api.SetFileAttributes(desktop_ini, win32con.FILE_ATTRIBUTE_HIDDEN + win32con.FILE_ATTRIBUTE_SYSTEM)
                win32api.SetFileAttributes(parent, win32con.FILE_ATTRIBUTE_READONLY)
                print(parent)
        except:
            pass
#reset('C:/Users/17402/Desktop/爬虫/save/anime')
