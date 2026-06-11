import re
from setuptools import setup, find_packages

with open('scalekit/_version.py') as f:
    __version__ = re.search(r"^__version__ = ['\"]([^'\"]+)['\"]", f.read(), re.M).group(1)

setup(

    name="scalekit-sdk-python",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "grpcio>=1.81.0",
        "protobuf>=5.29.5,<7.0.0",
        "google>=3.0",
        "requests>=2.34.0",
        "PyJWT>=2.13.0",
        "cffi>=1.15.1",
        "cryptography==46.0.6,<47",
        "setuptools>=78.1.1,<83.0",
        "grpcio-status>=1.81.0,<2.0",
        "protoc-gen-openapiv2>=0.0.1",
        "googleapis-common-protos>=1.72.0",
        "deprecation>=2.1.0",
        "python-dotenv>=1.1.1,<2.0",
        "Faker>=33.0.0,<41.0",
        "pydantic>=2.10.6",
        "mcp>= 1.23.0",
    ],
    url="https://github.com/scalekit-inc/scalekit-sdk-python",
    license="MIT",
    author="Team Scalekit",
    author_email="support@scalekit.com",
    description="Scalekit official Python SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
