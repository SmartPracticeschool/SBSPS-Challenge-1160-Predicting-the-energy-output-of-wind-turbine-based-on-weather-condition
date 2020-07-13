# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()
long_description = "This app has been designed as the UI for the project in IBM Hack Challenge 2020. The Dash module with plotly python is used for the development process."

setup(
    name='ibmhc',
    version='1.0.0',
    description='UI for the IBM Hack Challenge 2020',
    long_description=long_description,
    url='https://github.com/SmartPracticeschool/SBSPS-Challenge-1160-Predicting-the-energy-output-of-wind-turbine-based-on-weather-condition',
    license='Apache-2.0'
)