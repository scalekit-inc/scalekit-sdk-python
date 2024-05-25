from setuptools import setup, find_packages

setup(
    name='scalekitSDKPython',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'grpcio==1.64.0',
        'protobuf==5.27.0',
        'google==3.0.0',
        'requests==2.32.2',
        'PyJWT==1.7.1',
        'authlib==1.3.0',
        'setuptools==69.2.0'
    ],
    url='https://github.com/scalekit-inc/scalekit-sdk-python',
    license='',
    author='Scalekit-Inc',
    author_email='support@scalekit.com',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
