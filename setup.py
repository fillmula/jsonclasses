"""setup.py"""
from pathlib import Path
from setuptools import setup, find_packages

# The text of the README file
README = (Path(__file__).parent / "README.md").read_text()

setup(
    name='jsonclasses',
    version='3.0.0',
    description=('The modern declarative data flow pipeline and data graph '
                 'framework for the AI empowered generation.'),
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
    python_requires='>=3.10',
    install_requires=[]
)
