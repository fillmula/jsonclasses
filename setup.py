"""setup.py"""
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='jsonclasses',
    version='2.5.0',
    description=('The Modern Declarative Data Flow and Data Graph Framework '
                 'for the AI Empowered Generation.'),
    long_description=README,
    long_description_content_type='text/markdown',
    author='Fillmula Inc.',
    author_email='victor.teo@fillmula.com',
    license='MIT',
    packages=find_packages(exclude=('tests')),
    package_data={'jsonclasses': ['py.typed']},
    zip_safe=False,
    url='https://github.com/fillmula/jsonclasses',
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=['inflection>=0.5.1,<1.0.0'])
