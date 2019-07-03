__author__="tomkow"
__date__ ="$6-May-2011 3:00:55 PM$"

from setuptools import setup,find_packages

setup (
  name = 'AIshooter',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'Craig Ttomkow',
  author_email = 'ctomkow@gmail.com',

  summary = 'Just another Python package for the cheese shop',
  url = 'http://www.craigsite.ca/',
  license = '',
  long_description= 'Long description of the package',

  # could also include long_description, download_url, classifiers, etc.

  
)