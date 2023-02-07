from setuptools import setup, find_packages

setup(
    name='fast-resource',
    version='0.1.0',
    author='Bagher Rokni',
    author_email='bagher.rokni@gmail.com',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    url='https://github.com/bagher/fast-resource',
    license='LICENSE.txt',
    description='fast-resource is a data transformation layer between the database and data returned to the '
                'application\'s users. Also, it can cache data by using Redis and Memcached.',
    long_description=open('README.md').read(),
    install_requires=['redis', 'pymemcache'],
    long_description_content_type='text/markdown',
    python_requires='>=3.*',
)
