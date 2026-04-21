import setuptools

setuptools.setup(
    name="DemoPackage",
    version="0.0.7",
    author="DigiNova",
    author_email='info@diginova.com.tr',
    description="Test Package",
    url='https://github.com/CengizOkan/demo2',
    license='MIT',
    install_requires=[], # TAMAMEN BOŞ
    packages=[
        'components.DemoPackage.src',
        'components.DemoPackage.src.executors',
        'components.DemoPackage.src.models',
        'components.DemoPackage.src.utils',
    ],
    package_dir={'components.DemoPackage.src': 'src'},
    python_requires=">=3.6"
)