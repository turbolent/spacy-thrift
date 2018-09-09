#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='spacy-thrift',
      version='0.5.0',
      description='spaCy-as-a-service using Thrift',
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords=["natural language processing", "nlp"],
      url='https://github.com/turbolent/spacy-thrift',
      author='Bastian Mueller',
      author_email='bastian@turbolent.com',
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Topic :: Text Processing",
      ],
      packages=['spacyThrift'],
      install_requires=[
          "click==6.7",
          "thrift==0.11.0",
          "spacy==2.0.12",
          "coloredlogs==10.0"
      ])
