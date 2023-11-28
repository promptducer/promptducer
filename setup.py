from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_ = f.read()

setup(
    name='evaluator',
    version='0.1.0',
    description='sedGPT Evaluator',
    long_description=readme,
    author='SED',
    author_email='sed@sed.sed',
    url='https://sed.hu',
    license=license_,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'promptducer=promptducer.main:main'
        ]
    },
)
