import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='jsonclasses',
  version='0.5.1',
  description='The Modern Declarative Data Flow Framework for the AI Empowered Generation.',
  long_description=README,
  long_description_content_type='text/markdown',
  author='Wiosoft Crafts',
  author_email='wiosoftvictor@163.com',
  license='MIT',
  packages=find_packages(exclude=('tests', 'benchmarks', 'examples')),
  zip_safe=False,
  url='https://github.com/Wiosoft-Crafts/jsonclasses',
  include_package_data=True,
  python_requires='>=3.8',
  install_requires=[
    'inflection>=0.5.1,<1.0.0'
  ]
)
