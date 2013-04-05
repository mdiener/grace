from glob import glob
import os
from distutils.core import setup
import sys

if os.name == 'nt':
    sys.path.append('C:\\Program Files (x86)\\Microsoft Visual Studio 11.0\\VC\\redist\\x86\\Microsoft.VC110.CRT')
    data_files = [('Microsoft.VC110.CRT', glob(r'C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\redist\x86\Microsoft.VC110.CRT\*.*'))]
else:
    data_files = []

setup(
    name='grace',
    description='A tool to simplify JavaScript development.',
    author='Michael Diener',
    author_email='dm.menthos@gmail.com',
    url='https://github.com/mdiener/grace',
    version='0.1',
    packages=['grace']
)
