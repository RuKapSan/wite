from setuptools import setup

setup(
    name="wite",
    version="0.1.0",
    py_modules=["wite"],  # Должен соответствовать имени файла wite.py
    entry_points={
        'console_scripts': [
            'wite=wite:main',
        ],
    },
    install_requires=[],
)
