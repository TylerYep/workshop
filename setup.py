import setuptools

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="typorch",
    version="0.0.1",
    author="Tyler Yep",
    author_email="tyep10@gmail.com",
    description="Dynamic Shape/Type Checking for PyTorch",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/tyleryep/workshop",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
