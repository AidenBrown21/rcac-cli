from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="rcac-cli",
        version="0.1.0",
        packages=find_packages(),
        install_requires=[
            "requests",
            "rich",
            "pydantic",
            "regex",
        ],
        entry_points={
            "console_scripts": [
                "rcac=rcac_cli.main:_handle_cli_args",
            ]
        },
        python_requires=">=3.9",
    )
