import setuptools

setuptools.setup(
    name="DemoPackage",
    version="0.0.1",
    author="Cengiz",
    description="Demo Package for NovaVision",
    # 'sdk' yazan hatalı kısmı kaldırdık, sadece gerçekten gerekenleri bıraktık
    install_requires=['opencv-python-headless', 'numpy'],
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)