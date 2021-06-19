import os
import re
import requests
import shutil
import sys

root_path = sys.path[0]


def mkdir(relative_path):
    path = os.path.join(root_path, "downloads", relative_path)
    folder = os.path.exists(path)
    if not folder:
        os.mkdir(path)
        return True

    else:
        return False


def cleandir(relative_path):
    path = os.path.join(root_path, "downloads", relative_path)
    folder = os.path.exists(path)
    if folder:
        # 存在文件夹 另起内部文件
        shutil.rmtree(path)
        os.mkdir(path)
        return True


def download(url, relative_path):
    print(re.match("http: | https:", url, re.M | re.I))
    if not re.match("http:|https:", url, re.M | re.I):
        url = f"https:{url}"
    name = re.findall(r'[^\\/:*?"<>|\r\n]+$', url)[0]
    path = os.path.join(root_path, "downloads", relative_path, name)
    r = requests.get(url)
    with open(path, "wb") as image:
        image.write(r.content)
        return True
