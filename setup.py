from setuptools import setup


setup(
   name='transcribepods',
   version='0.1',
   description='Module to download and transcribe podcasts.',
   long_description="",
   url="",
   author='Arnold Freitas',
   packages=['transcribepods'],  # same as name
   # external packages as dependencies
   install_requires=[
                    "selenium",
                    "transformers",
                    ], 
)
