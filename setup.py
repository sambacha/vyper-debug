#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    "test": ["pytest==4.2.0", "pytest-xdist", "tox>=2.9.1,<3",],
    "lint": ["flake8==3.4.1", "isort>=4.2.15,<5",],
    "dev": [
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "twine",
        "ipython",
    ],
}

extras_require["dev"] = (
    extras_require["dev"]
    + extras_require["test"]
    + extras_require["lint"]
)

setup(
    name="vyper-debug",
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version="0.1.2-beta.7",
    description="""vyper-debug: Easy to use Vyper debugger | vdb""",
    long_description_markdown_filename="README.md",
    author="Jacques Wagener",
    author_email="jacques+pip@dilectum.co.za",
    url="https://github.com/ethereum/vyper-debug",
    include_package_data=True,
    install_requires=[
        "py-evm==0.2.0a34",
        "eth-tester==0.1.0b33",
        "vyper>=0.1.0b8",
        "web3==4.8.1",
    ],
    setup_requires=["setuptools-markdown"],
    python_requires=">=3.6, <4",
    extras_require=extras_require,
    py_modules=["vdb"],
    license="MIT",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    scripts=["bin/vyper-run",],
)
