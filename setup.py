from setuptools import setup, find_packages
from platform import system


_system = system()

install_requires = []
if _system == 'Windows':
 install_requires += [
 #'pywin32',
 'libloader'
]

__doc__ = 'Library to provide speech and braille output to a variety of different screen readers and other accessibility solutions.',

with open('readme.rst') as readme:
 long_description = readme.read()

setup(
 name = 'accessible_output2',
 author = 'Tyler Spivey',
 author_email = 'tspivey@pcdesk.net',
 version='0.12.dev0',
 description = __doc__,
 long_description = long_description,
 package_dir = {'accessible_output2': 'accessible_output2'},
 packages = find_packages(),
 package_data = {"accessible_output2": ["lib/*"]},
 zip_safe = False,
 classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows',
  'Programming Language :: Python',
  'License :: OSI Approved :: MIT License',
'Topic :: Adaptive Technologies',
'Topic :: Software Development :: Libraries'
],
 install_requires = install_requires,
)
