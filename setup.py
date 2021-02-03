import setuptools

__version__ = "1.4.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymee",
    version=__version__,
    author="FreshlyBrewedCode",
    description="a python library to interact with homee",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FreshlyBrewedCode/pymee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)