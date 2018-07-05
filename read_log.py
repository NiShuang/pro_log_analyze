# -*- coding: UTF-8 -*-

import re
import sys
import os
import json
from config import config

reload(sys)
sys.setdefaultencoding("utf-8")

log_path = config['log_path']

def read_log(filename):
    with open(filename, 'r') as log_file:
         lines = log_file.readlines()

    pattern1 = re.compile('INFO\s+\[----MESSAGE----\]\sseq:\d+\s(\{.+?})\ssystem/inspro')
    pattern2 = re.compile('INFO\s+send\smsg\sseq:\d+\scontent\slen:\d+\scontent:(\{.+?})\ssystem/inspro')
    pattern3 = re.compile('INFO\s+\[----MESSAGE----\]\s(\{.+?})\ssystem/inspro')

    json_list = []

    for line in lines:
        # print line
        result = re.findall(pattern1, line)
        try:
            if len(result) > 0:
                json_list.append(json.loads(result[0].replace('\t','')))
            else:
                result = re.findall(pattern2, line)
                if len(result) > 0:
                    json_list.append(json.loads(result[0].replace('\t','')))
                else:
                    result = re.findall(pattern3, line)
                    if len(result) > 0:
                        json_list.append(json.loads(result[0].replace('\t','')))
        except:
            continue
    # print filename, len(json_list)
    return json_list

## abandon
def read_logs(size):
    result = []
    log_list = os.listdir(log_path)
    count = 0
    for log in log_list:
        file_path = os.path.join(log_path, log)
        if os.path.isfile(file_path):
            json_list = read_log(file_path)
            result.extend(json_list)
        count += 1
        if count == size:
            break

    return result

def get_file_list():
    file = open('data/file_used.json', 'r')
    file_used = set(json.load(file))
    file.close()
    result = []
    log_list = os.listdir(log_path)
    for log in log_list:
        file_path = os.path.join(log_path, log)
        if os.path.isfile(file_path) and (not file_path in file_used):
            result.append(file_path)
    print len(result)
    return result, file_used


if __name__ == '__main__':
    # read_log('data/1523675283041.log')
    pass