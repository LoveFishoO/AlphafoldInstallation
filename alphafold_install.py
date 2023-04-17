import os
import re
import requests

import subprocess as sp

from lxml import etree


PATH = os.path.dirname(__file__)


def get_linux_bit():
    linux_bit_cmd = sp.Popen(['getconf', 'LONG_BIT'], stdout=sp.PIPE)
    linux_bit = linux_bit_cmd.stdout.read().decode().replace('\n','')
    return linux_bit

def list_find(lst, pattern):
    
    for s in lst:
        
        if re.search(pattern, s):
            return s
    return None

def install_make():
    
    try:
        sp.run('cmake -h', shell=True, check=True, stdout=sp.PIPE)
        
        cmake_version_cmd = sp.run(['cmake', '--version'], stdout=sp.PIPE)

        cmake_version = cmake_version_cmd.stdout.decode().split('\n')[0]
        
        print(f'cmake had been installed: {cmake_version}')
        
    except:
        
        # crawl url
        url, makefilename = get_make_url()
        print(f'cmake download url: {url}')
        
        # download cmake file
        print('start to download cmake')
        sp.run(['wget', '-q', '-O', f'{PATH}/cmake.tar.gz', '-c', url], stdout=sp.PIPE)
        print('cmake complete download')
        
        # unzip
        print('start to unzip cmake')
        sp.run(['tar', '-zxvf', f'{PATH}/cmake.tar.gz'], stdout=sp.PIPE)
        print('decompression complete')
        
        # compile and install
        dirname = list_find(os.listdir(PATH), 'cmake-')
        os.chdir(f'{PATH}/{dirname}')
        sp.run(['./bootstrap'])
        sp.run(['make'])
        sp.run(['make install'])
        
        # check 
        try:
            sp.run(['cmake', '-h'], check=True, stdout=sp.PIPE)
            print('cmake installation succeeds\n')
        except:
            print('cmake installation failure\n')
        
        os.chdir(PATH)
        
    return None

def get_make_url():
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }

    resp = requests.get(url="https://cmake.org/download/", headers=headers)

    html_etree = etree.HTML(resp.text.encode('utf-8'))
    
    filename = html_etree.xpath('/html/body/div/div/div/article/div/div/div/div/div/div[2]/div/div[1]/div/table[1]/tbody/tr[2]/td[2]/a/text()')[0]
    url = html_etree.xpath('/html/body/div/div/div/article/div/div/div/div/div/div[2]/div/div[1]/div/table[1]/tbody/tr[2]/td[2]/a/@href')[0]

    return url, filename

