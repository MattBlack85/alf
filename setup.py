import os
from setuptools import setup


def read_md(f):
    return open(f, 'r', encoding='utf-8').read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name='alf',
    version='0.0.1',
    description='App to send local logs to a remote server using AsyncIO',
    long_description=read_md('README.md'),
    author='Den Automation Ltd.',
    author_email='cloud-devs@getden.co.uk',
    packages=get_packages('alf'),
    package_data=get_package_data('den_notifications'),
    install_requires=[
        'aiohttp>=3.4',
        'aiodns>=1.1',
        'cchardet>=2.1',
    ],
    zip_safe=False,
    scripts=[
        'bin/alf'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: AsyncIO',
        'Intended Audience :: Developers',
        'Operating System :: GNU/Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Logs',
    ]
)
