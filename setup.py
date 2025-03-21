from setuptools import setup, find_packages

setup(
    name="scalekit-sdk-python",
    version="1.0.6",
    packages=find_packages(),
    install_requires=[
        "grpcio>=1.64.1",
        "protobuf>=5.27.0",
        "google>=3.0",
        "requests>=2.32.3",
        "PyJWT>=2.8,<2.10",
        "cryptography==44.0.0",
        "setuptools~=70.3",
        "grpcio-status>=1.64,<1.67",
        "protoc-gen-openapiv2>=0.0.1",
        "googleapis-common-protos>=1.56.1,<1.66.0",
        "deprecation>=2.1.0",
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
