import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="grammar-lab",
    version="0.0.1",
    author="Miroslav Harag",
    author_email="miroslavharag01@gmail.com",
    description="grammar lab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages()
)