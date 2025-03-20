from setuptools import setup, find_packages

setup(
    name="paper_checker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'python-docx',
        'langdetect',
        'httpx',
        'pyyaml'
    ],
)