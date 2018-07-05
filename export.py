# -*- coding: UTF-8 -*-

import collections
import json
import sys

from config.remark import remark
from utils.utils import write_result
from utils.utils import list_cmp,list_cmp1

try:
    import cPickle as pickle
except ImportError:
    import pickle
reload(sys)
sys.setdefaultencoding("utf-8")


with open('data/result', 'r') as f:
    result = pickle.load(f)

def write_basic():
    content = '发起拍照： name 值为 camera._takePicture' + '\n\n'
    content += ''
    for index, item in enumerate(result['take_count']):
        content += remark[0][index] + ':\t' + str(item) + '\n'

    content += '\n\n' + '————————————————' + '\n\n'

    content += '录像 name 值为 camera._startRecording' + '\n\n'
    content += ''
    for index, item in enumerate(result['record_count']):
        content += remark[1][index] + ':\t' + str(item) + '\n'

    content += '\n\n' + '————————————————' + '\n\n'

    content += '直播 name 值为 camera._startLive' + '\n\n'
    content += ''
    for index, item in enumerate(result['live_count']):
        content += remark[2][index] + ':\t' + str(item) + '\n'

    content += '\n\n' + '————————————————' + '\n\n'

    write_result('output/result1.txt', content)

#####
    content = ''
    content += '发起拍照： name 值为 camera._takePicture wb、aaa_mode频次统计\n\n'

    for index in result['option_count']['wb']:
        content += 'wb = ' + str(index) + ':\t' + str(result['option_count']['wb'][index]) + '\n'

    content += '\n\n' + '————————————————' + '\n\n'

    for index in result['option_count']['aaa_mode']:
        content += 'aaa_mode = ' + str(index) + ':\t' + str(result['option_count']['aaa_mode'][index]) + '\n'

    write_result('output/result2.txt', content)

def write_recording():
    record_option = result['record_option']

    new_record_option = []
    for item in record_option:
        finish = False
        item['wb']  = list(item['wb'])
        item['aaa_mode']  = list(item['aaa_mode'])
        for new_item in new_record_option:
            if cmp(new_item['data']['wb'], item['wb'])==0 and cmp(new_item['data']['aaa_mode'], item['aaa_mode'])==0:
                new_item['count'] += 1
                finish = not finish
                break
        if not finish:
            new_record_option.append(
                {
                    'data': item,
                    'count': 1
                }
            )

    new_record_option.sort(cmp=list_cmp)

    content = ''
    content += '每一次录像： name 值为camera._startRecording，和 camera._stopRecording。过程出现的参数：\n\n'
    for item in new_record_option:
        content += json.dumps(item['data']) + ' :\t' + str(item['count']) + '\n'
    write_result('output/result3.txt', content)

def write_live():
    live_option = result['live_option']
    new_live_option = []

    for item in live_option:
        finish = False
        item['wb'] = list(item['wb'])
        item['aaa_mode'] = list(item['aaa_mode'])
        for new_item in new_live_option:
            if cmp(new_item['data']['wb'], item['wb']) == 0 and cmp(new_item['data']['aaa_mode'], item['aaa_mode']) == 0:
                new_item['count'] += 1
                finish = True
                break
        if not finish:
            new_live_option.append(
                {
                    'data': item,
                    'count': 1
                }
            )

    new_live_option.sort(cmp=list_cmp)

    content = ''
    content += '每一次直播： name 值为camera._startLive，和 camera._stopLive。过程出现的参数：\n\n'
    for item in new_live_option:
        content += json.dumps(item['data']) + ' :\t' + str(item['count']) + '\n'
    write_result('output/result4.txt', content)

def write_timelapse():
    timelapse_option = result['timelapse_option']
    new_timelapse_option = {
        'option': [],
        'interval': collections.OrderedDict()
    }

    for item in timelapse_option['option']:
        finish = False
        item['wb'] = list(item['wb'])
        item['aaa_mode'] = list(item['aaa_mode'])
        for new_item in new_timelapse_option['option']:
            if cmp(new_item['data']['wb'], item['wb']) == 0 and cmp(new_item['data']['aaa_mode'], item['aaa_mode']) == 0 and cmp(new_item['data']['long_shutter'], item['long_shutter']) == 0:
                new_item['count'] += 1
                finish = True
                break
        if not finish:
            temp = collections.OrderedDict()
            temp['wb'] = item['wb']
            temp['aaa_mode'] = item['aaa_mode']
            temp['long_shutter'] = item['long_shutter']
            new_timelapse_option['option'].append(
                {
                    'data': temp,
                    'count': 1
                }
            )

    new_timelapse_option['option'].sort(cmp=list_cmp1)

    sorted_key_list = sorted(timelapse_option['interval'])

    for key in sorted_key_list:
        new_timelapse_option['interval'][key] = timelapse_option['interval'][key]

    print new_timelapse_option['interval']

    content = ''
    content += '每一次Timelapse。过程出现的参数：\n\n'
    for item in new_timelapse_option['option']:
        content += json.dumps(item['data']) + ' :\t' + str(item['count']) + '\n'

    content += '\n\n' + '————————————————' + '\n\n'
    for index in new_timelapse_option['interval']:
        content += 'interval = ' + str(index) + ':\t' + str(new_timelapse_option['interval'][index]) + '\n'

    write_result('output/result5.txt', content)

def export():
    write_basic()
    write_timelapse()
    write_live()
    write_recording()
