from glob import glob
from distutils.core import setup
import sys
import py2exe
import os

sys.path.append('C:\\Program Files (x86)\\Microsoft Visual Studio 11.0\\VC\\redist\\x86\\Microsoft.VC110.CRT')
data_files = [
    ('Microsoft.VC110.CRT', glob(r'C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\redist\x86\Microsoft.VC110.CRT\*.*'))
]

previous = ''
for root, dirs, files in os.walk(os.path.join('grace_package', 'skeletons')):
    for filename in files:
        if previous != root:
            data_files.append((root, glob(root + '\*.*')))
            previous = root

setup(
    name='grace',
    description='A tool to simplify JavaScript development.',
    author='Michael Diener',
    author_email='dm.menthos@gmail.com',
    url='https://github.com/mdiener/grace',
    version='0.1',
    packages=['grace_package'],
    data_files=data_files,
    console=['grace.py'],
    install_requires=['libsass'],
    options={
        'py2exe': {
            'packages': ['grace_package'],
            'bundle_files': True,
            'includes': ['sass', 'plistlib']
        }
    }
)
