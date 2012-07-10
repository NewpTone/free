
fromm setuptools import setup, find_packages
setup(
name="free memory command tool",
version="0.10",
description="A MACH Version of *inx memory command tool free",
author="Newptone",
url="http://www.cnblogs.com/yuxc",
license="LGPL",
packages= find_packages(),
scripts=["free.py"],
)
