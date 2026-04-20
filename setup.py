import setuptools

setuptools.setup(
    name="ImageProcessor",
    version="0.0.1",
    author="DigiNova",
    author_email='info@diginova.com.tr',
    description="Image Filter and Compare Package",
    url='https://github.com/CengizOkan/demo2',
    license='MIT',
    install_requires=['sdk', 'opencv-python-headless', 'numpy'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=[
        'novavision.ImageProcessor',
        'novavision.ImageProcessor.executors',
        'novavision.ImageProcessor.models',
        'novavision.ImageProcessor.utils',
    ],
    package_dir={'novavision.ImageProcessor': 'src'},
    python_requires=">=3.6"
)