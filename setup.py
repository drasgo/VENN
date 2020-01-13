try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="ViCreNN",
    version="0.5.0",
    author="Drasgo",
    author_email="tommasocastiglione@gmail.com",
    license=open('LICENSE').read(),
    description="Visual Editor of Neural Networks",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/drasgo/ViCreNN",
    packages=["ViCreNN", "ViCreNN/gui", "ViCreNN/nn", ],
    install_requires=['PyQt5'],
    extras_require={
        'TensorFlow': ['tensorflow'],
        'PyTorch': ['torch', "torchsummary"],
        'Keras': ['keras'],
        'FastAI': ['fastai'],
	'Documentation': ['pdoc'] 
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC BY-NC 4.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
