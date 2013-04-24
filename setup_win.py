from glob import glob
from distutils.core import setup
import sys
import py2exe
import os

sys.path.append(os.path.join(os.getcwd(), 'grace'))
sys.path.append(os.path.join('C:\\Python27\\Scripts'))
sys.path.append('C:\\Program Files (x86)\\Microsoft Visual Studio 11.0\\VC\\redist\\x86\\Microsoft.VC110.CRT')
data_files = [('Microsoft.VC110.CRT', glob(r'C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\redist\x86\Microsoft.VC110.CRT\*.*'))]

setup(
    name='grace',
    description='A tool to simplify JavaScript development.',
    author='Michael Diener',
    author_email='dm.menthos@gmail.com',
    url='https://github.com/mdiener/grace',
    version='0.1',
    package=['grace'],
    data_files=data_files,
    console=['grace/main.py']
)
