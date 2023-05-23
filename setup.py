"""Setup file"""
from setuptools import setup  # type: ignore

VERSION = "1.3.7"

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setup(name="hibpwned",
      packages=["hibpwned"],
      version=VERSION,
      description="A human friendly Python API wrapper for haveibeenpwned.com",
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      author="plasticuproject",
      author_email="plasticuproject@pm.me",
      url="https://github.com/plasticuproject/hibpwned",
      download_url="https://github.com/plasticuproject/hibpwned/archive/v" +
      VERSION + ".tar.gz",
      keywords=["hibp", "haveibeenpwned", "api", "wrapper"],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v3" +
          " or later (GPLv3+)", "Programming Language :: Python :: 3",
          "Topic :: Communications :: Chat", "Topic :: Utilities"
      ],
      license="GPLv3",
      install_requires=["requests"],
      zip_safe=False,
      include_package_data=True)
