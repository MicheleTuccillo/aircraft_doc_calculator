from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="doc_calculator",
    version="0.3.0",
    packages=find_packages(),
    install_requires = ["gemseo"],
    long_description=description,
    long_description_content_type="text/markdown"

)