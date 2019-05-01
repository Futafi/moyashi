from setuptools import setup
VERSION ="0.0.1"

setup(
        name="moyashi",
        packages=["moyashi"],
        version=VERSION,
        install_requires=[
            "beautifulsoup4",
            "requests"
            ]
        )
