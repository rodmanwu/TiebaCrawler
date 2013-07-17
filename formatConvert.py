# -*- coding=utf-8 -*-
__author__ = 'rodmanwu'

import os
import os.path

from_suffix = '.jpg'
to_suffix = '.gif'

for root,dir,files in os.walk('E:\TiebaCrawler'):
    for file in files:
        # 注意这里如果直接用 file会出问题
        # http://stackoverflow.com/questions/5324107/windowserror-error-2-the-system-cannot-find-the-file-specified
        filename = os.path.join(root,file)
        if filename.endswith(from_suffix):
            os.rename(filename,filename.replace(from_suffix,to_suffix))

