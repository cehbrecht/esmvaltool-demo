import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

reqs = [line.strip() for line in open('requirements/deploy.txt')]

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
]

setup(name='esmvalwps',
      version='1.0.1',
      description='WPS processes for ESMValTool',
      long_description=README + '\n\n' + CHANGES,
      classifiers=classifiers,
      author='Birdhouse',
      author_email='',
      url='http://www.esmvaltool.org/',
      license="Apache License v2.0",
      keywords='wps pywps conda birdhouse esmvaltool',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='esmvalwps',
      install_requires=reqs,
      entry_points={
          'console_scripts': []
      },
      )
