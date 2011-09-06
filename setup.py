#!/usr/bin/env python

from setuptools import setup

setup(name='TweetFS',
      version='0.1',
      description='Clandestinely store small files and directories on Twitter.',
      author='Robert Winslow',
      author_email='robert.winslow@gmail.com',
      url='http://github.com/rw/tweetfs',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: End Users/Desktop',
                   'Natural Language :: English',
                   'Programming Language :: Python',
                   'Topic :: Text Processing :: Filters',
                   'Topic :: Text Processing :: Linguistic',
                  ],
      requires=['bitstring', 'Plainsight (==1.1.2)', 'SeqTweet (==0.1)'],
      scripts=['bin/tweetfs'],
      packages=['tweetfs']
     )
