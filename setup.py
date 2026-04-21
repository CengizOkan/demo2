import setuptools

setuptools.setup(
    name="DemoPackage",
    version="0.1.0",
    author="Cengiz Okan",
    packages=setuptools.find_namespace_packages(include=["components.*"]),
    install_requires=[
        'numpy',
        'pydantic',
        'opencv-python-headless' # Docker içinde hata vermemesi için headless sürüm
    ],
    python_requires=">=3.8"
)