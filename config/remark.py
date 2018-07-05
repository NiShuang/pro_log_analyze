# -*- coding: UTF-8 -*-

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

remark = [
    [
        '总数',
        'stiching里 mode 为 pano 的数量',
        'stiching里 mode 为 3d_top_left 的数量',
        'origin 里 mime 为 jpeg 的数量',
        'origin 里 mime 为 raw 的数量',
        '有 stiching 这条属性的数量',
        'burst 里 enable 为 true 的数量',
        'hdr 里 enable 为 true 的数量'
    ],

    [
        '总数',
        '有 stiching这个属性但为空，或没有stiching属性的数量',
        'stiching里 mode 为 pano 的数量',
        'stiching里 mode 为 3d_top_left 的数量',
        'origin 里 width 为1920 且 height 为 1440 的数量',
        'origin 里 width 为3200 且 height 为 2400 的数量',
        'origin 里 width 为3840 且 height 为 2160 且 framerate 为30的数量',
        'origin 里 width 为3840 且 height 为 2160 且 framerate 为5的数量',
        'origin 里 width 为2560 且 height 为 1440 的数量',
        'logMode 为1的数量',
        'timelapse 属性 enable 为 true 的数量'
    ],

    [
        '总数',
        'stiching 属性中，liveOnHdmi 值为 true 的数量',
        'stiching 属性中，_liveUrl 以 rtsp 开头的字符串的数量',
        'stiching 属性中，_liveUrl 以 rtmp 开头的字符串的数量',
        'stiching 属性中，mode 为 pano 的数量',
        'stiching 属性中，mode 为 3d_top_left 的数量',
        'stiching 属性中，fileSave 为 true 的数量',
        'origin 属性中，saveOrigin为 true 的数量'
    ]

]