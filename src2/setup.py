from setuptools import setup, find_packages

setup(
    name="deep_learning_api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.15.0',
        'flask>=3.0.0',
        'pytest>=7.4.3',
        'requests>=2.31.0',
        'numpy>=1.26.2',
        'pandas>=2.1.4',
        'matplotlib>=3.8.2',
        'scikit-learn>=1.3.2',
    ],
    python_requires='>=3.8',
)