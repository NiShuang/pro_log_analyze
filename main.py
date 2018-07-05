# -*- coding: UTF-8 -*-

from analyze_log import LogAnalyzer
from export import  export
import sys


reload(sys)
sys.setdefaultencoding("utf-8")

log_analyzer = LogAnalyzer()
log_analyzer.start_analyze()

export()
