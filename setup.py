from setuptools import setup

setup(name='comidatweet',
      version='1.0',
      description='OpenShift App',
      author='Jesus Bueno',
      author_email='example@123.com',
      url='comidatweet-jesusba.rhcloud.com',
      install_requires=[
	'bottle',
	'python-requests',
	'requests',
	'requests-oauthlib',
	'oauthlib',
	],
     )
