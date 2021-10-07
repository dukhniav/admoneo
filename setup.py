#from distutils.core import setup
import setuptools

setuptools.setup(
    name='analyzer',
    version='0.0.1',
    packages=['analyzer', ],
    license='MIT',
    description='Python script to continuously analyze crypto data.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Artem Dukhnitskiy',
    author_email='dukhnitskiy@gmail.com',
    install_requires=['requests'],
    url='https://github.com/dukhniav/analyzer',
)
