from setuptools import find_packages, setup

from mario import __version__

# load readme
with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="mario",
    version=__version__,
    description="Make kubeflow pipelines intuitive.",
    packages=find_packages(exclude=["tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["kfp", "kubernetes", "yaml"],
    license="MIT",
)
