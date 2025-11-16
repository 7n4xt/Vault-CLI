from setuptools import setup

setup(
    name="vault-cli",
    version="0.1.0",
    description="Simple encrypted vault CLI",
    packages=["src"],
    package_dir={"src": "src"},
    include_package_data=True,
    install_requires=[
        "cryptography",
    ],
    entry_points={
        "console_scripts": [
            "vault-cli=src.cli:main",
        ]
    },
    python_requires=">=3.10",
)
