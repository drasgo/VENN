try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="VENN",
    version="1.0.0",
    author="Drasgo",
    author_email="tommasocastiglione@gmail.com",
    license=open('LICENSE').read(),
    description="Visual Editor of Neural Networks",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/drasgo/VENN",
    packages=["VENN", "VENN/gui", "VENN/nn"],
    install_requires=['PyQt5'],
    extras_require={
        'TensorFlow': ['tensorflow'],
        'PyTorch': ['torch', "torchsummary"],
        'Keras': ['keras'],
#       'FastAI': ['fastai'],
	    'Documentation': ['pdoc'],
        'Pytorch Visualization': ['torchsummary']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC BY-NC 4.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
