from glob import glob
import os
from setuptools import setup

package_data = {'grace': []}

previous = ''
for root, dirs, files in os.walk(os.path.join('grace', 'skeleton')):
    for filename in files:
        if previous != root:
            filelist = glob(root + '/*.*')
            for f in filelist:
                package_data['grace'].append(f[6:])
            previous = root

for root, dirs, files in os.walk(os.path.join('grace', 'assets')):
    for filename in files:
        if previous != root:
            filelist = glob(root + '/*.*')
            for f in filelist:
                package_data['grace'].append(f[6:])
            previous = root

setup(
    name='grace',
    description='A tool to simplify JavaScript development.',
    author='Michael Diener',
    author_email='michael@webdiener.ch',
    url='https://github.com/mdiener/grace',
    version='0.4.23',
    license='LICENSE.txt',
    scripts=['bin/grace'],
    packages=['grace'],
    install_requires=['pyScss', 'argparse', 'setuptools', 'slimit', 'cssmin', 'pyjsdoc', 'requests', 'watchdog', 'gitpython', 'CoffeeScript'],
    package_data=package_data,
    keywords='toolchain javascript dizmo js buildtool',
    long_description=open('README.txt').read(),
    classifiers=[
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: JavaScript',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Developers',
        'Environment :: Console'
    ]
)
