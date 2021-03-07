from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="event_scheduler",
    version="0.0.1",
    author="Dil Mchaina, Farhan Ahmed, PhluentMed",
    author_email="phluentmed@gmail.com",
    description="Always-on event scheduler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phluentmed",
    packages=find_packages(),
    keywords='Python Event Scheduler',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)