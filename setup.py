import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymolPy3",
    version="0.1.2",
    author="Cong Wang",
    author_email="wangimagine@gmail.com",
    description="A PyMOL wrapper in Python3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carbonscott/pymolPy3",
    keywords = ['PDB', 'structure biology', 'protein', 'molecular graphics'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
