from glob import glob
from distutils.core import setup
import sys
import py2exe
import os

sys.path.append(os.path.join(os.getcwd(), 'grace'))
sys.path.append('C:\\Python27\\Scripts')
sys.path.append('C:\\Python27\\Lib\\site-packages')
sys.path.append('C:\\Program Files (x86)\\Microsoft Visual Studio 11.0\\VC\\redist\\x86\\Microsoft.VC110.CRT')
data_files = [
    ('Microsoft.VC110.CRT', glob(r'C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\redist\x86\Microsoft.VC110.CRT\*.*')),
    ('plugins', glob(os.path.join('grace', 'plugins') + '\*.py'))
]

previous = ''
for root, dirs, files in os.walk(os.path.join('grace', 'skeletons')):
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
    version='0.1',
    packages=['grace'],
    data_files=data_files,
    console=['grace/grace.py'],
    options={
        'py2exe': {
            'packages': ['grace'],
            'bundle_files': True,
            'includes': ['grace.build', 'grace.deploy', 'grace.error', 'grace.create', 'grace.task', 'grace.testit', 'grace.zipit', 'sass', 'plistlib']
        }
    }
)
