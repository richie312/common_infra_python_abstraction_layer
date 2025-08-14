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
    license_file="LICENSE",
    python_requires=">=3.7",  # Specify the minimum Python version
    install_requires=[
        "confluent-kafka","flask",
        "redis"
    ]
)