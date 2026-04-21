import setuptools

setuptools.setup(
    name="DemoPackage",
    version="0.0.1",
    author="DigiNova",
    author_email='info@diginova.com.tr',
    description="Image Filter and Compare Package",
    url='https://github.com/CengizOkan/demo2',
    license='MIT',
    install_requires=['sdk', 'opencv-python-headless', 'numpy'],
    packages=[
        'novavision.DemoPackage',
        'novavision.DemoPackage.executors',
        'novavision.DemoPackage.models',
        'novavision.DemoPackage.utils',
    ],
    package_dir={'novavision.DemoPackage': 'src'},
    python_requires=">=3.6"
)