import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="unisgf",
    version="0.0.1",
    author="Shevela Roman",
    author_email="goglbummm@gmail.com",
    description="SGF parser and renderer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pymole/unisgf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)