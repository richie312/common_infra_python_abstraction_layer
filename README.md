## Common Infrastructure Python Abstraction Library

This library will be used for multiple applications to interact with common infrastructure like kafka, redis, database and other components.

## dokcer run command

docker run -d -p 5003:5003 --name common_infra_abstraction_layer --network my_rasp_network --restart unless-stopped richie31/common_infra

## library build

1. Write setup.py file

```
from setuptools import setup, find_packages

setup(
    name="common_infra_python_library",  # Replace with your package name
    version="1.0.0",  # Replace with your package version
    author="Richie312",  # Replace with your name
    author_email="richie.chatterjee31@gmail.com",  # Replace with your email
    description="Python Library for Common Infrastructure Components like Redis, Kafka, sql, etc",  # Short description
    long_description=open("README.md").read(),  # Use README.md for the long description
    long_description_content_type="text/markdown",  # Specify the format of the long description
    url="https://github.com/richie312/common_infra_python_abstraction_layer",  # Replace with your project's URL
    packages=find_packages(),  # Automatically find and include all packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Specify the minimum Python version
    install_requires=[
        "confluent-kafka","flask",
        "redis"
    ]
)
```

2. Build Your Python Library
On your Windows development machine:

Navigate to the directory containing your Python library's setup.py file.
Build the library:
This will create a .tar.gz file in the dist/ directory.
Alternatively, if you're using pyproject.toml (modern packaging):


```
python setup.py sdist bdist_wheel
```

3. Install twine for Uploading
Ensure twine is installed on your Windows machine:

```
pip install twine
```

4. Upload the Library to the Local PyPI Server
Use twine to upload the built package to the PyPI server running on 192.168.1.4:

```
twine upload --repository-url http://192.168.1.4:8080/ dist/*
```

Replace 8080 with the port your PyPI server is running on.
The dist/* refers to all built packages in the dist directory.
5. Install the Library from the Local PyPI Server
To install the library from the local PyPI server on any machine in the network:

```
pip install --index-url http://192.168.1.4:8080/ <package-name>
```

