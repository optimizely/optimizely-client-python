from setuptools import setup

setup(name='optimizely',
      version='0.4',
      description='A Python interface to Optimizely\'s REST API.',
      url='https://github.com/optimizely/optimizely-client-python',
      author='Optimizely',
      author_email='developers@optimizely.com',
      packages=['optimizely'],
      keywords=['python-sdk', 'optimizely'],
      download_url='https://github.com/optimizely/optimizely-client-python/tarball/0.3',
      install_requires=[
        'requests',
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
