import setuptools

packages = [
        "simplejson",
        "strict-rfc3339",
        "apache_beam"
        ]

setuptools.setup(
    install_requires=packages,
    packages=setuptools.find_packages(),
)