import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Event-Scheduler-pkg-Phluent_Med",
    version="0.0.1",
    author="PhluentMed",
    author_email="PhluentMed@gmail.com",
    description="Non-stop running event scheduler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phluentmed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #TODO get actual license figured out
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)