from setuptools import setup, find_packages

def update_octets(version_string):
    # Split the IP address into octets
    octets = list(map(int, version_string.split('.')))

    # Check if the third octet reaches 10
    octets[2] += 1  # Reset the third octet

    if octets[2] >= 10:
        octets[1] += 1  # Reset the third octet
        octets[2] = 10

    if octets[1] >= 10:  # Increment the second octet
        octets[0] +=1
        octets[1] = 10

        # Ensure the second octet does not exceed 255
        if octets[0] >= 1:
            octets[1] = 0
            octets[2] = 0

    # Reconstruct the updated version
    updated_version = '.'.join(map(str, octets))
    return updated_version


setup(
    name="common_infra_python_library",  # Replace with your package name
    version=update_octets("1.0.1"),  # Replace with your package version
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
