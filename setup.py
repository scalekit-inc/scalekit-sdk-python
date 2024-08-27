from setuptools import setup, find_packages

setup(
    name="scalekit-sdk-python",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "grpcio~=1.64.1",
        "protobuf~=5.27.0",
        "google~=3.0.0",
        "requests~=2.32.3",
        "PyJWT~=2.8.0",
        "cryptography~=42.0.8",
        "setuptools~=70.3.0",
        "grpcio-status~=1.64.0",
        "protoc-gen-openapiv2~=0.0.1",
        "googleapis-common-protos~=1.56.1",
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
