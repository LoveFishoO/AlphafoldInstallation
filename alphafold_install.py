import os
import re
import sys
import requests

import subprocess as sp

from lxml import etree

PYTHON = sys.executable
PATH = os.path.dirname(__file__)
CUDA12 = '12.0'
CUDA11 = '11.0'

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
        
        apt_install(packname='cmake')
        
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


def install_hmmer():
    try:
        hmmer_cmd =  sp.run('jackhmmer -h', shell=True, check=True, stdout=sp.PIPE)

        hmmer_version = hmmer_cmd.stdout.decode().split('\n')[1]

        print(f'hmmer had been installed: {hmmer_version}')
    
    except:
        
        # install hmmer
        print('start to install hmmer')
        sp.run(['sudo','apt', 'install', 'hmmer'])
        print('installation completed')

        # check 
        try:
            sp.run(['jackhmmer', '-h'], check=True, stdout=sp.PIPE)
            print('hmmer installation succeeds\n')
        except:
            print('hmmer installation failure\n')
        
    return None


def install_hhsuite():
    
    try:
        
        hhsuite_cmd = sp.run(['hhblits', '-h'], check=True, stdout=sp.PIPE, stderr=sp.PIPE)
        hhsuite_version = hhsuite_cmd.stdout.decode().split('\n')[0][:-1]
        
        print(f'hh-suite had been installed: {hhsuite_version}')
        
    except:
        print('start to clone hh-suite')
        sp.run(['git', 'clone', 'https://github.com/soedinglab/hh-suite.git'])
        print('clone hh-suite complete')
        
        print('start to compile and install')
        sp.run(['mkdir', '-p', f'{PATH}/hh-suite/build'])
        
        os.chdir(f'{PATH}/hh-suite/build/')
        
        sp.run(['cmake', '-DCMAKE_INSTALL_PREFIX=/usr/local/', '..'])
        
        sp.run(['make', '-j', '4'])
        
        sp.run(['sudo', 'make', 'install'])
        print('hh-suite installation complete ')
        
        try:
            sp.run(['hhblits', '-h'], check=True, stdout=sp.PIPE)
            print('hh-suite installation succeeds\n')
        except:
            print('hh-suite installation failure\n')
        
        os.chdir(PATH)
 
    return None


def install_kalign():
    
    try:
        
        kalign_cmd = sp.run(['kalign', '-h'], check=True, stdout=sp.PIPE, stderr=sp.PIPE)
        kalign_version = kalign_cmd.stdout.decode().split('\n')[1]

        print(f'kalign had been installed: {kalign_version}')
    
    except:
        
        sp.run(['wget', '-O', f'{PATH}/kalign.tar.gz', '-c', 'https://github.com/TimoLassmann/kalign/archive/refs/tags/v3.3.5.tar.gz'])
        
        # unzip
        print('start to unzip kalign')
        sp.run(['tar', '-zxvf', f'{PATH}/kalign.tar.gz'], stdout=sp.PIPE)
        print('decompression complete')

        # compile and install
        dirname = list_find(os.listdir(PATH), 'kalign-')
        
        print('start to compile and install')
        sp.run(['mkdir', '-p', f'{PATH}/{dirname}/build'])
        os.chdir(f'{PATH}/{dirname}/build')
        sp.run(['cmake', '..'])
        sp.run(['make'])
        sp.run(['sudo', 'make', 'install'])
        
        try:
            sp.run(['kalign', '-h'], check=True, stdout=sp.PIPE)
            print('kalign installation succeeds\n')
        except:
            print('kalign installation failure\n')
        
        os.chdir(PATH)
        
    return None

def install_openmm():
    
    try:
        # sudo apt install doxygen, swig
        openmm_cmd = sp.run([PYTHON, '-m', 'openmm.testInstallation'], check=True, stdout=sp.PIPE)
        openmm_version = openmm_cmd.stdout.decode().split('\n')[1]

        print(f'kalign had been installed: {openmm_version}')
    
    except:
        
        sp.run(['wget', '-O', f'{PATH}/openmm.tar.gz', '-c','https://github.com/openmm/openmm/archive/refs/tags/8.0.0.tar.gz'])

        # unzip
        print('start to unzip openmm')
        sp.run(['tar', '-zxvf', f'{PATH}/openmm.tar.gz'], stdout=sp.PIPE)
        print('decompression complete')

        # install dependency
        apt_install('doxygen')
        apt_install('swig')
        
        # compile and install
        dirname = list_find(os.listdir(PATH), 'openmm-')

        print('start to compile and install')
        
        sp.run(['mkdir', '-p', f'{PATH}/{dirname}/build'])
        os.chdir(f'{PATH}/{dirname}/build')
        sp.run(['cmake', '..'])
        sp.run(['make'])
        sp.run(['sudo', 'make', 'install'])
        
        sp.run(['sudo', PYTHON, '-m', 'pip', 'install', 'numpy', 'cython'])
        sp.run(['sudo', 'make', 'PythonInstall'])
        
        try:
            sp.run([PYTHON, '-m', 'openmm.testInstallation'], check=True, stdout=sp.PIPE)
            print('openmm installation succeeds\n')
        except:
            print('openmm installation failure\n')

        os.chdir(PATH)
        
    return None

def apt_install(packname):

    sp.run(['sudo', 'apt', 'install', packname])
    
    return None

def install_pdbfixer():
    
    print('start to install pdbfixer')
    sp.run(['sudo', PYTHON, '-m', 'pip', 'install','git+http://github.com/openmm/pdbfixer.git'])

    print('pdbfixer installation complete')  
    return None


def install_software():
    
    install_lists = [install_make, install_hmmer, install_hhsuite, install_kalign, install_openmm, install_pdbfixer]
    
    for func in install_lists:
        
        func()
        
    return None

def get_cuda_version():
    nvidia_cmd = sp.run(
        ['nvidia-smi', '-q', '-d', 'compute'], check=True, stdout=sp.PIPE)
    cuda_version_infos = nvidia_cmd.stdout.decode().split('\n')[5]
    cuda_version = cuda_version_infos.split()[-1]

    if cuda_version == CUDA12:
        return CUDA12
    elif cuda_version == CUDA11:
        return CUDA11
    else:
        raise ValueError(f'This cuda version({cuda_version}) is not supported')


def install_packages():
    
    print('start to install python packages')
    
    print('start to upgrade pip')
    sp.run([PYTHON, '-m', 'pip', 'install', '--user', '-U', 'pip'])
    print('pip upgrade complete')
    
    # read python package info
    with open(os.path.join(PATH, 'requirements.txt'), 'r') as rf:
        
        packages_infos = rf.readlines()
    
    for package in packages_infos:
        
        package = package.strip()
        
        # TODO Conflict resolution
        print(f'start to install {package}')
        sp.run([PYTHON, '-m', 'pip', 'install', '--user', package])
        print(f'{package} installation complete')
        
    # install jax
    cuda_version = get_cuda_version()
    
    if cuda_version == CUDA12:
        
        print(f'start to install JAX, CUDA version is {CUDA12}')
        sp.run(f'{PYTHON} -m pip install --user "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html', shell=True)
        print(f'JAX installation complete')
    
    elif cuda_version == CUDA11:
        
        print(f'start to install JAX, CUDA version is {CUDA11}')
        sp.run(f'{PYTHON} -m pip install --user "jax[cuda11_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html', shell=True)
        print(f'JAX installation complete')
        
    else:
        
        raise ValueError(f'This cuda version({cuda_version}) is not supported')
    
    return None


def main():
    
    functions = [install_software, install_packages]
    
    for func in functions:
        
        func()
    
    return None

if __name__ == '__main__':
    
    main()