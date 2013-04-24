from glob import glob
from distutils.core import setup
import sys
import py2app
import os

sys.path.append(os.path.join(os.getcwd(), 'grace'))
data_files = [
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
