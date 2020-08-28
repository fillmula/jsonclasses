from setuptools import setup

setup(name='jsonclasses',
  version='0.1',
  description='Python dataclass & json interchangeable.',
  author='Wiosoft Crafts',
  author_email='wiosoftvictor@163.com',
  license='MIT',
  packages=['jsonclasses'],
  zip_safe=False,
  url='https://github.com/Wiosoft-Crafts/jsonclasses',
  include_package_data=True,
  python_requires='>=3.6',
  install_requires=[
    'inflection>=0.5.1,<1.0.0'
  ]
)
