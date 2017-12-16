#!/usr/bin/env python

from setuptools import setup

setup(name='spacy-thrift',
      version='0.4.0',
      description='spaCy-as-a-service using Thrift',
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
          "thrift==0.10.0",
          "spacy==2.0.5",
          "coloredlogs==7.3.1"
      ])
