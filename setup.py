import setuptools


with open('README.md') as fh:
    long_description = fh.read()

NAME = 'pyparsedvd'
VERSION = '0.0.2'

setuptools.setup(
    name=NAME,
    version=VERSION,
    author='Vardë',
    author_email='ichunjo.le.terrible@gmail.com',
    description='Parse and extract binary data from dvd files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pyparsedvd', 'pyparsedvd.vts_ifo'],
    package_data={
        'pyparsedvd': ['py.typed'],
    },
    url='https://github.com/Ichunjo/pyparsedvd',
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
