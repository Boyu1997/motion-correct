import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="motion-correct",
    version="0.0.1",
    author="Boyu Jiang",
    author_email="jbyjiangboyu@126.com",
    description="Use motion information to correct face recognition result.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boyu1997",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
