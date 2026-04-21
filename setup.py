import setuptools

setuptools.setup(
    name="DemoPackage",
    version="0.1.0",
    author="Cengiz Okan",
    packages=[
        "components",
        "components.DemoPackage",
        "components.DemoPackage.src",
        "components.DemoPackage.src.models",
        "components.DemoPackage.src.executors",
        "components.DemoPackage.src.utils"
    ],
    install_requires=[
        'numpy',
        'pydantic',
        'opencv-python-headless'
    ],
    python_requires=">=3.8"
)