import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='fetch',
    version='0.0.2',
    author='Gergely Dervarics',
    author_email='dervarics@gmail.com',
    description='http request wrapper with simple caching',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/greg76/fetch',
    project_urls = {
        "Bug Tracker": "https://github.com/greg76/fetch/issues"
    },
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[],
)