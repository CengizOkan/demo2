import setuptools

setuptools.setup(
    name="DemoPackage",
    version="0.1.0",
    author="DigiNova",
    description="NovaVision Specification Compliant Package",
    packages=setuptools.find_namespace_packages(include=["components.*"]),
    install_requires=['numpy', 'pydantic'],
    python_requires=">=3.6"
)