from setuptools import find_packages, setup

# load readme
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="mario",
    version="0.0.1",
    description="Make kubeflow pipelines intuitive.",
    packages=find_packages(exclude=["tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["kfp"],
    license="MIT",
)
