from setuptools import setup, find_packages

setup(

    name="scalekit-sdk-python",
    version="2.4.10",
    packages=find_packages(),
    install_requires=[
        "grpcio>=1.64.1",
        "protobuf<6.0.0,>=5.26.1",
        "google>=3.0",
        "requests>=2.32.3",
        "PyJWT>=2.8,<2.10",
        "cffi>=1.15.1",
        "cryptography==45.0.6",
        "setuptools>=78.1.1",
        "grpcio-status>=1.64,<1.67",
        "protoc-gen-openapiv2>=0.0.1",
        "googleapis-common-protos>=1.56.1,<1.66.0",
        "deprecation>=2.1.0",
        "python-dotenv>=1.1.0",
        "Faker~=25.8.0",
        "pydantic>=2.10.6",
        "mcp>= 1.15.0",
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