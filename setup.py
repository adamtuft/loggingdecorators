from setuptools import find_packages, setup

version = (0,1,0)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="loggingdecorators",
    version=".".join(map(str, version)),
    author="Adam Tuft",
    author_email='adam.s.tuft@gmail.com',
    description="NONE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms=["linux"],
    url="https://github.com/adamtuft/loggingdecorators",
    packages=find_packages()
)
