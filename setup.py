from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='fastshield',
  version='0.0.2',
  author='ilpdakz',
  author_email='khasanknyazev81@gmail.com',
  description='library to protect your fastapi applications',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/knyazevi81/fastshield',
  packages=find_packages(),
  install_requires=[
    'requests>=2.25.1',
    'scikit-learn==1.5.1'
  ],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/knyazevi81'
  },
  python_requires='>=3.6'
)