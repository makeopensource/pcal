from setuptools import setup

setup(
  name='Pcal',
  version='0.1.0',
  py_modules=['pcal'],
  install_requires=[
    'Click',
  ],
  entry_points='''
    [console_scripts]
    pcal=pcal:cli
  ''',
)