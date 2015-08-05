from setuptools import setup

setup(name='optimizely',
      version='0.1',
      description='An interface to Optimizely\'s REST API.',
      url='https://github.com/optimizely/optimizely-client-python',
      author='Optimizely',
      packages=['optimizely'],
      install_requires=[
        'requests',
      ],
      zip_safe=False,
      test_suit='nose.collector',
      tests_require=['nose'])