# -*- coding: UTF-8 -*-

import os
import sys
import zipfile

import requests

from config.config import config
from utils.multi_thread import WorkManager

reload(sys)
sys.setdefaultencoding("utf-8")

zip_path = config['zip_path']
log_path = config['log_path']
log_url_file = config['log_url_file']
thread_num = config['thread_num']

def get_log_urls():
    with open(log_url_file, 'r') as log_file:
         urls = log_file.read().split('\n')
    urls.pop()
    return urls


def download_and_unzip(url):
    filename = url[-17:]
    r = requests.get(url)
    file_path = zip_path + filename
    with open(file_path, 'wb') as f:
        f.write(r.content)
    unzip(filename)


def unzip(filename):
    try:
        zip_file = zipfile.ZipFile(zip_path + filename)
    except:
        print 'wrong file:' + filename
        return
    if len(zip_file.namelist()) > 1:
        new_path = log_path + filename[:-4]
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        zip_file.extractall(new_path)
    else:
        zip_file.extractall(log_path)

def start_download():
    urls = get_remaining_urls()
    for url in urls:
        download_and_unzip(url)


def get_remaining_urls():
    zip_list = os.listdir(zip_path)
    zip_set = set(zip_list)
    urls = get_log_urls()
    i = 0
    while i < len(urls):
        if urls[i][-17:] in zip_set:
            del urls[i]
            i -= 1
        i += 1
    print len(urls)
    return urls


def start_multi_thread_download():
    urls = get_remaining_urls()
    wm = WorkManager(thread_num)
    for index, i in enumerate(urls):
        wm.add_job(index, download_and_unzip, i)
    wm.start()
    wm.wait_for_complete()



if __name__ == '__main__':
    # start_download()
    pass
