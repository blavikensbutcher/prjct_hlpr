from setuptools import setup, find_namespace_packages

setup(
    name="console_assistant",
    version="0.0.1",
    description="console_assistant",
    url="https://github.com/blavikensbutcher",
    author="blavikensbutcher",
    license="MIT",
    packages=find_namespace_packages(),
    install_requires=["prettytable", "prompt_toolkit"],
    entry_points={"console_scripts": ["assistant = src.main:main"]},
)
