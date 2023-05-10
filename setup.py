import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="grammarlab",
    version="0.0.1",
    author="Miroslav Harag",
    author_email="miroslavharag01@gmail.com",
    description="grammar lab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages()
)
