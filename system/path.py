import os
import re
import sys

root_path = sys.path[0]


def get_image_path(page_id, url):
    name = re.findall(r'[^\\/:*?"<>|\r\n]+$', url)[0]
    image_path = os.path.join(root_path, "downloads", page_id, name)
    if os.path.exists(image_path):
        return os.path.join(root_path, "downloads", page_id, name)
    else:
        return False


def get_save_image_path(name):
    return os.path.join(root_path, "downloads", name)
