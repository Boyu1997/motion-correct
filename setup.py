import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="motion-correct",
    version="0.0.1",
    author="Boyu Jiang",
    author_email="jbyjiangboyu@126.com",
    description="Extract motion information to improve face recognition accuracy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Boyu1997/motion-correct",
    python_requires='>=3.6',
    install_requires=['numpy', 'tensorflow', 'keras'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
