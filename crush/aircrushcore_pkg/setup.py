import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aircrushcore",
    version="0.1.20",
    author="Dave Mattie",
    author_email="dmattie@stfx.ca",
    description="Core pipelines and operators for airCRUSH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmattie/aircrushcore",
    project_urls={
        "Bug Tracker": "https://github.com/dmattie/aircrushcore/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    #packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)