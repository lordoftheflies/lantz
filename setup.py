#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from distutils.util import convert_path

try:
    from setuptools import setup
except ImportError:
    print('Please install or upgrade setuptools or pip to continue')
    sys.exit(1)

import os
import codecs


def read(filename):
    return codecs.open(filename, encoding='utf-8').read()


long_description = '\n\n'.join([read('README.rst'),
                                read('AUTHORS'),
                                read('CHANGES')])

__doc__ = long_description

requirements = []

if sys.version_info < (3, 4):
    requirements.append('enum34')

root_folder = os.path.dirname(os.path.abspath(__file__))

# Compile a list of companies with drivers.
folder = os.path.join(root_folder, 'lantz', 'drivers')
paths = os.listdir(folder)
companies = [path for path in paths
             if os.path.isdir(os.path.join(folder, path))
             and os.path.exists(os.path.join(folder, path, '__init__.py'))]

# Compile a list of companies with legacy drivers.
folder = os.path.join(root_folder, 'lantz', 'drivers', 'legacy')
paths = os.listdir(folder)
legacy_companies = [path for path in paths
                    if os.path.isdir(os.path.join(folder, path))
                    and os.path.exists(os.path.join(folder, path, '__init__.py'))]

# ========================================
# Version parsing
# ========================================
main_ns = {}
ver_path = convert_path('version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(name='Lantz',
      version=main_ns['__version__'],
      license='Apache 2.0 License',
      description='Instrumentation framework',
      long_description=long_description,
      keywords='measurement control instrumentation science',
      author='lordoftheflies',
      author_email='laszlo.hegedus@cherubits.hu',
      url='https://github.com/lordoftheflies/lantz/',
      packages=['lantz',
                'lantz.ui',
                'lantz.ui.blocks',
                'lantz.simulators',
                'lantz.utils',
                'lantz.drivers'] +
               ['lantz.drivers.' + company for company in companies] +
               ['lantz.drivers.legacy.' + company for company in legacy_companies],
      test_suite='lantz.testsuite.testsuite',
      install_requires=['pint>=0.6',
                        'pyvisa>=1.6.2',
                        'stringparser',
                        ] + requirements,
      zip_safe=False,
      platforms='any',
      entry_points={
          'zest.releaser.releaser.after_checkout': [
              'pyroma = lantz:run_pyroma',
          ],
          'console_scripts': [
              'lantz-sim = lantz.simulators:main',
          ]
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development :: Libraries'
      ],
      scripts=[
          'scripts/lantz-monitor',
      ])
