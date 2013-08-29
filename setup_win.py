from glob import glob
from distutils.core import setup
import sys
import py2exe
import os

sys.path.append('C:\\Program Files (x86)\\Microsoft Visual Studio 11.0\\VC\\redist\\x86\\Microsoft.VC110.CRT')
package_data = {'grace': []}
data_files = [
    ('Microsoft.VC110.CRT', glob(r'C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\redist\x86\Microsoft.VC110.CRT\*.*'))
]

previous = ''
for root, dirs, files in os.walk(os.path.join('grace', 'skeleton')):
    for filename in files:
        if previous != root:
            data_files.append((root[6:], glob(root + '\*.*')))
            previous = root

setup(
    name='grace',
    description='A tool to simplify JavaScript development.',
    author='Michael Diener',
    author_email='dm.menthos@gmail.com',
    url='https://github.com/mdiener/grace',
    version='0.1.17',
    license='LICENSE.txt',
    packages=['grace'],
    data_files=data_files,
    console=['bin/grace'],
    keywords='toolchain javascript dizmo js buildtool',
    long_description=open('README.txt').read(),
    options={
        'py2exe': {
            'packages': ['grace'],
            'bundle_files': True
        }
    }
)
