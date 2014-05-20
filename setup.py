from setuptools import setup
import oauthlib

setup(name='comidatweet',
      version='1.0',
      description='OpenShift App',
      author='Jesus Bueno',
      author_email='example@123.com',
      url='comidatweet-jesusba.rhcloud.com',
      install_requires=[
	'bottle',
	'json',
	'requests',
	'requests_oauthlib'],
     )
