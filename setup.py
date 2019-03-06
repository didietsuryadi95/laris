from os.path import dirname, join, abspath
from setuptools import find_packages, setup

ROOT_DIR = dirname(abspath(__file__))

setup(
    packages=find_packages(where=join(ROOT_DIR, 'src/testimo/')),
    package_dir={'testimo': 'src/testimo/'},
    include_package_data=True,
    scripts=['src/testimo/manage.py']
)
