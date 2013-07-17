# coding=utf-8
__author__ = 'rodmanwu'


import  requests
import lxml.html
import os
from urlparse import urlparse


class NetworkError(RuntimeError):
   def __init__(self, arg):
      self.args = arg

def preprocessUrl(raw_url):
    """ Return the protocol , hostname[,port] and  path of url,
    parameters , query and fragment will be removed

    :param raw_url: raw url string

    >>> preprocessUrl('http://tieba.baidu.com/p/2090361112?pn=1')
    'http://tieba.baidu.com/p/2090361112'
    """
    parse_url = urlparse(raw_url)
    cleaned_url = []
    if parse_url.scheme is not '':
        cleaned_url.append(parse_url.scheme)
        cleaned_url.append('://')

    cleaned_url.append(parse_url.netloc)
    cleaned_url.append(parse_url.path)
    return ''.join(cleaned_url)


def mkdir(path):

    path = path.strip()
    path = path .strip('\\')

    isExist = os.path.exists(path)

    if not isExist:
        print '[Create Folder]  ' + path
        os.makedirs(path)


def downloadImages(url):     # tieba url

    base_url = preprocessUrl(url)
    failed_log = []

    # Crawl images from each page
    # Start from page 1 , stop when page is not accessible
    for i in xrange(1,100):
        url = base_url + '?pn=' + str(i)

        # Check web page accessible
        status = requests.head(url).status_code
        if status is not 200:
            print "[DownLoad Finish]"
            break

        # web page source code
        page_content = requests.get(url).text
        print '[Start DownLoad] ' + url

        # convert to html format
        doc = lxml.html.document_fromstring(page_content)

        # web page title ,use for root folder
        title_folder = doc.find('.//title').text
        mkdir(title_folder)

        # create folder for each page
        page_folder = title_folder + os.sep + 'Page_'+str(i)
        mkdir(page_folder)

        for idx , el in enumerate(doc.cssselect('img.BDE_Image')):
            try:
                response = requests.get(el.attrib['src'])
                if response.status_code is not 200:
                    failed_log.append(el.attrib['src'])
                    print '[Failed] ' + el.attrib['src']
                else:
                    with open(page_folder + os.sep +'%04d.jpg' % idx ,'wb') as f:
                        f.write(response.content)
            except :
                failed_log.append(el.attrib['src'])
                print '[Failed] ' + el.attrib['src']

    if len(failed_log) > 0:
        with open('failed_log.txt','w') as f:
            for failed_item in failed_log:
                f.writelines(failed_item)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    downloadImages('http://tieba.baidu.com/p/2090361112?pn=1')