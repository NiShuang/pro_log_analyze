# -*- coding: UTF-8 -*-

from read_log import read_log, get_file_list
from utils.utils import write_file, serialize_result, merge_dict
import json
import sys

try:
    import cPickle as pickle
except ImportError:
    import pickle

reload(sys)
sys.setdefaultencoding("utf-8")


class LogAnalyzer:
    def __init__(self):
        self.result_list = []

    def analyze_log(self, filename):
        json_list = read_log(filename)

        take_count = []
        for i in range(0, 8):
            take_count.append(0)

        record_count = []
        for i in range(0, 11):
            record_count.append(0)

        live_count = []
        for i in range(0, 8):
            live_count.append(0)

        option_count = {
            'wb': {},
            'aaa_mode': {}
        }

        record_option = []
        live_option = []
        timelapse_option = {
            'interval': {},
            'option': []
        }

        is_recording = False
        is_live = False
        is_timelapse_recording = False

        for index, item in enumerate(json_list):
            if item['name'] == 'camera._takePicture' and item.has_key('parameters'):
                take_count[0] += 1

                parameters = item['parameters']

                if parameters.has_key('origin'):
                    origin = parameters['origin']

                    if origin.has_key('mime') and origin['mime']=='jpeg':
                        take_count[3] += 1

                    if origin.has_key('mime') and origin['mime']=='raw':
                        take_count[4] += 1

                if parameters.has_key('stiching'):
                    take_count[5] += 1

                    stiching = parameters['stiching']

                    if stiching.has_key('mode') and stiching['mode']=='pano':
                        take_count[1] += 1

                    if stiching.has_key('mode') and stiching['mode']=='3d_top_left':
                        take_count[2] += 1

                if parameters.has_key('burst') and parameters['burst'].has_key('enable') and parameters['burst']['enable']:
                    take_count[6] += 1

                if parameters.has_key('hdr') and parameters['hdr'].has_key('enable') and parameters['hdr']['enable']:
                    take_count[7] += 1

                for i in range(index - 1 ,-1,-1):
                    temp_item = json_list[i]

                    if temp_item['name'] == 'camera._getImageParam' and temp_item.has_key('results'):
                        results = temp_item['results']
                        wb_count = results['wb']
                        aaa_mode_count = results['aaa_mode']
                        if option_count['wb'].has_key(wb_count):
                            option_count['wb'][wb_count] += 1
                        else:
                            option_count['wb'][wb_count] = 1

                        if option_count['aaa_mode'].has_key(aaa_mode_count):
                            option_count['aaa_mode'][aaa_mode_count] += 1
                        else:
                            option_count['aaa_mode'][aaa_mode_count] = 1
                        break


            if item['name'] == 'camera._startRecording' and item.has_key('parameters'):
                record_count[0] += 1

                parameters = item['parameters']

                if (not parameters.has_key('stiching')) or len(parameters['stiching']) == 0:
                    record_count[1] += 1

                else:
                    if parameters['stiching']['mode'] == 'pano':
                        record_count[2] += 1

                    if parameters['stiching']['mode'] == '3d_top_left':
                        record_count[3] += 1

                if parameters.has_key('origin'):
                    origin = parameters['origin']

                    if origin['width']==1920 and origin['height']==1440:
                        record_count[4] += 1

                    if origin['width']==3200 and origin['height']==2400:
                        record_count[5] += 1

                    if origin['width']==3840 and origin['height']==2160 and origin['framerate']==30:
                        record_count[6] += 1

                    if origin['width']==3840 and origin['height']==2160 and origin['framerate']==5:
                        record_count[7] += 1

                    if origin['width']==2560 and origin['height']==1440:
                        record_count[8] += 1

                    if origin.has_key('logMode') and origin['logMode'] == 1:
                        record_count[9] += 1

                if parameters.has_key('timelapse') and parameters['timelapse']['enable']:
                    record_count[10] += 1
                    if not is_timelapse_recording:
                        is_timelapse_recording = True
                        timelapse_temp = {
                            'wb': set(),
                            'aaa_mode': set(),
                            'long_shutter': {}
                        }

                        if parameters['timelapse'].has_key('interval'):
                            interval_value = parameters['timelapse']['interval']
                            if timelapse_option['interval'].has_key(interval_value):
                                timelapse_option['interval'][interval_value] += 1
                            else:
                                timelapse_option['interval'][interval_value] = 1


                        for i in range(index - 1, -1, -1):
                            temp_item = json_list[i]
                            if temp_item['name'] == 'camera._getImageParam' and temp_item.has_key('results'):
                                results = temp_item['results']
                                wb_count = results['wb']
                                aaa_mode_count = results['aaa_mode']
                                timelapse_temp['wb'].add(wb_count)
                                timelapse_temp['aaa_mode'].add(aaa_mode_count)
                                long_shutter = results['long_shutter']
                                if timelapse_temp['long_shutter'].has_key(long_shutter):
                                    timelapse_temp['long_shutter'][long_shutter] += 1
                                else:
                                    timelapse_temp['long_shutter'][long_shutter] = 1
                                break

                if not is_recording:
                    is_recording = True
                    record_temp = {
                        'wb': set(),
                        'aaa_mode': set()
                    }

                    for i in range(index - 1, -1, -1):
                        temp_item = json_list[i]
                        if temp_item['name'] == 'camera._getImageParam' and temp_item.has_key('results'):
                            results = temp_item['results']
                            wb_count = results['wb']
                            aaa_mode_count = results['aaa_mode']
                            record_temp['wb'].add(wb_count)
                            record_temp['aaa_mode'].add(aaa_mode_count)


            if item['name'] == 'camera._startLive' and item.has_key('parameters'):
                live_count[0] += 1

                parameters = item['parameters']

                if parameters.has_key('stiching'):
                    stiching = parameters['stiching']

                    if stiching.has_key('liveOnHdmi') and stiching['liveOnHdmi']:
                        live_count[1] += 1

                    if stiching.has_key('_liveUrl') and stiching['_liveUrl'].startswith('rtsp'):
                        live_count[2] += 1

                    if stiching.has_key('_liveUrl') and stiching['_liveUrl'].startswith('rtmp'):
                        live_count[3] += 1

                    if stiching.has_key('mode') and stiching['mode']=='pano':
                        live_count[4] += 1

                    if stiching.has_key('mode') and stiching['mode']=='3d_top_left':
                        live_count[5] += 1

                    if stiching.has_key('fileSave') and stiching['fileSave']:
                        live_count[6] += 1

                if parameters.has_key('origin') and parameters['origin'].has_key('saveOrigin') and parameters['origin']['saveOrigin']:
                    live_count[7] += 1

                if not is_live:
                    is_live = True
                    live_temp = {
                        'wb': set(),
                        'aaa_mode': set()
                    }

                    for i in range(index - 1, -1, -1):
                        temp_item = json_list[i]
                        if temp_item['name'] == 'camera._getImageParam' and temp_item.has_key('results'):
                            results = temp_item['results']
                            wb_count = results['wb']
                            aaa_mode_count = results['aaa_mode']
                            live_temp['wb'].add(wb_count)
                            live_temp['aaa_mode'].add(aaa_mode_count)


            if item['name'] == 'camera._getImageParam' and item.has_key('results'):
                results =  item['results']
                try:
                    wb_count = results['wb']
                    aaa_mode_count = results['aaa_mode']
                    long_shutter = results['long_shutter']
                except:
                    continue

                if is_recording:
                    record_temp['wb'].add(wb_count)
                    record_temp['aaa_mode'].add(aaa_mode_count)

                if is_live:
                    live_temp['wb'].add(wb_count)
                    live_temp['aaa_mode'].add(aaa_mode_count)

                if is_timelapse_recording:
                    timelapse_temp['wb'].add(wb_count)
                    timelapse_temp['aaa_mode'].add(aaa_mode_count)
                    if timelapse_temp['long_shutter'].has_key(long_shutter):
                        timelapse_temp['long_shutter'][long_shutter] += 1
                    else:
                        timelapse_temp['long_shutter'][long_shutter] = 1


            if item['name'] == 'camera._stopRecording' and len(item)==1:
                if is_recording:
                    is_recording = False
                    if not (len(record_temp['wb']) == 0 and len(record_temp['aaa_mode']) == 0):
                        record_option.append(record_temp)

                if is_timelapse_recording:
                    is_timelapse_recording = False
                    if not (len(timelapse_temp['wb']) == 0 and len(timelapse_temp['aaa_mode']) == 0 and len(timelapse_temp['long_shutter']) == 0):
                        timelapse_option['option'].append(timelapse_temp)

            if item['name'] == 'camera._stopLive' and len(item)==1:
                if is_live:
                    is_live = False
                    if not (len(live_temp['wb']) == 0 and len(live_temp['aaa_mode']) == 0):
                        live_option.append(live_temp)


        result = {
            'take_count': take_count,
            'record_count': record_count,
            'live_count': live_count,
            'option_count': option_count,
            'record_option': record_option,
            'live_option': live_option,
            'timelapse_option': timelapse_option,
        }
        self.result_list.append(result)


    def get_sum(self):
        take_count = []
        for i in range(0, 8):
            take_count.append(0)

        record_count = []
        for i in range(0, 11):
            record_count.append(0)

        live_count = []
        for i in range(0, 8):
            live_count.append(0)

        option_count = {
            'wb': {},
            'aaa_mode': {}
        }
        record_option = []
        live_option = []
        timelapse_option = {
            'option': [],
            'interval': {}
        }
        for item in self.result_list:
            take_count = [take_count[i] + item['take_count'][i] for i in range(0, 8)]
            record_count = [record_count[i] + item['record_count'][i] for i in range(0, 11)]
            live_count = [live_count[i] + item['live_count'][i] for i in range(0, 8)]
            merge_dict(option_count['wb'], item['option_count']['wb'])
            merge_dict(option_count['aaa_mode'], item['option_count']['aaa_mode'])
            record_option.extend(item['record_option'])
            live_option.extend(item['live_option'])
            timelapse_option['option'].extend(item['timelapse_option']['option'])
            merge_dict(timelapse_option['interval'], item['timelapse_option']['interval'])

        result = {
            'take_count': take_count,
            'record_count': record_count,
            'live_count': live_count,
            'option_count': option_count,
            'record_option': record_option,
            'live_option': live_option,
            'timelapse_option': timelapse_option,
        }

        return result


    def print_export(self, result):
        print result['take_count']
        print result['record_count']
        print result['live_count']
        print result['option_count']
        for item in result['record_option']:
            print item
        print
        for item in result['live_option']:
            print item
        print
        for item in result['timelapse_option']['option']:
            print item
        print
        for item in result['timelapse_option']['interval']:
            print item


    def start_analyze(self):
        try:
            with open('data/result_save', 'r') as f:
                self.result_list.extend(pickle.load(f))
        except:
            serialize_result('data/result_save', [])
        file_list, file_used = get_file_list()
        for file in file_list:
            try:
                self.analyze_log(file)
            except:
                write_file('data/file_used.json', json.dumps(file_used))
                serialize_result('data/result_save', self.result_list)
                print 'Not finished'
                exit()
            file_used.append(file)
            write_file('data/file_used.json', json.dumps(file_used))

        serialize_result('data/result_save', self.result_list)
        result = self.get_sum()
        self.print_export(result)
        serialize_result('data/result', result)


