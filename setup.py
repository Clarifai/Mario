from setuptools import find_packages, setup

# load readme
with open("README.md", "r") as f:
    long_description = f.read()


def version() -> str:
    import mario

    return mario.__version__


setup(
    name="mario",
    version=version(),
    description="Make kubeflow pipelines intuitive.",
    packages=find_packages(exclude=["tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["kfp"],
    license="MIT",
)
