from setuptools import setup

version = '0.1.0'

setup(name='moco',
      version=version,
      description='DB-API 2.0 interface for ultramysql',
      author='Patrick Hull',
      author_email='patrick.d.hull@gmail.com',
      license='MIT',
      packages=['moco'],
      install_requires=['umysql'])
