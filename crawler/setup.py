from setuptools import setup, find_packages

setup(
    name="poe2db-crawler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.3",
        "pyppeteer>=1.0.2",
        "asyncio>=3.4.3",
    ],
    entry_points={
        'console_scripts': [
            'poe2db-crawler=cli:main',
        ],
    },
) 