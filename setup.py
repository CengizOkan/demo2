import setuptools

setuptools.setup(
    name="DemoPackage",
    version="0.0.8", # Versiyonu yeniledik
    author="DigiNova",
    author_email='info@diginova.com.tr',
    description="Image Filter and Compare Package (Pure Numpy)",
    url='https://github.com/CengizOkan/demo2',
    license='MIT',
    install_requires=['numpy'], # SADECE NUMPY
    packages=[
        'components.DemoPackage.src',
        'components.DemoPackage.src.executors',
        'components.DemoPackage.src.models',
        'components.DemoPackage.src.utils',
    ],
    package_dir={'components.DemoPackage.src': 'src'},
    python_requires=">=3.6"
)