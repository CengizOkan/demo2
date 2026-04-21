import setuptools

setuptools.setup(
    name="DemoPackage",
    version="1.0.0",
    author="Cengiz Okan",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pydantic',
        'opencv-python-headless'
    ],
    python_requires=">=3.8"
)