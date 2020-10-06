from distutils.core import setup

setup(
    name='pysetzer',
    version='1.0.0',
    packages=[
        'pysetzer',
    ],
    url='https://github.com/monolithos/pysetzer.git',
    license='COPYING',
    author='monolithos',
    author_email='capitan.develop@gmail.com',
    description='Python client for Setzer',
    install_requires=[
        'requests~=2.24.0',
    ],
)
