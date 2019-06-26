import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="docker-cp",
    version="0.1.0a1",
    author="Juliano Luiz Fernandes",
    author_email="julianofernandes@gmail.com",
    description="Copy files from or to a Docker container",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julianolf/docker-cp",
    packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
    ],
    keywords="docker cli copy",
    install_requires=["docker>=4.0.2", "docopt>=0.6.2", "schema>=0.7.0"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["docker-cp=docker_cp.cli:main"]},
)
