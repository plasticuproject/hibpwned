from setuptools import setup

version = '1.2.2'

setup(name='hibpwned',
      packages=['hibpwned'],
      version=version,
      description='A human friendly Python API wrapper for haveibeenpwned.com',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='plasticuproject',
      author_email='plasticuproject@pm.me',
      url='https://github.com/plasticuproject/hibpwned',
      download_url='https://github.com/plasticuproject/hibpwned/archive/v' + version + '.tar.gz',
      keywords=['hibp', 'haveibeenpwned', 'api', 'wrapper'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python :: 3',
          'Topic :: Communications :: Chat',
          'Topic :: Utilities'
      ],
      license='GPLv3',
      install_requires=['requests'],
      zip_safe=False,
include_package_data=True)
