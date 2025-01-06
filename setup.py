from distutils.version import LooseVersion
import os
import sys

from setuptools import __version__ as setuptools_version
from setuptools import find_packages
from setuptools import setup

version = '3.1.0.dev0'

# Remember to update local-oldest-requirements.txt when changing the minimum
# acme/certbot version.
install_requires = [
    'setuptools',
    'zope.interface',
    'requests>=2.4.2',
    'dns-lexicon>=3.15.1'
]

if not os.environ.get('SNAP_BUILD'):
    install_requires.extend([
        'acme>={version}',
        'certbot>={version}',
    ])
elif 'bdist_wheel' in sys.argv[1:]:
    raise RuntimeError('Unset SNAP_BUILD when building wheels '
                       'to include certbot dependencies.')
if os.environ.get('SNAP_BUILD'):
    install_requires.append('packaging')

setuptools_known_environment_markers = (LooseVersion(setuptools_version) >= LooseVersion('36.2'))
if setuptools_known_environment_markers:
    install_requires.append('mock ; python_version < "3.3"')
elif 'bdist_wheel' in sys.argv[1:]:
    raise RuntimeError('Error, you are trying to build certbot wheels using an old version '
                       'of setuptools. Version 36.2+ of setuptools is required.')
elif sys.version_info < (3,3):
    install_requires.append('mock')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='certbot-plugin-gandi',
    version=version,
    author="Yohann Leon",
    author_email="yohann@leon.re",
    description="Certbot plugin for authentication using Gandi LiveDNS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obynio/certbot-plugin-gandi",
    packages=find_packages(),
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        ],
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-gandi = certbot_plugin_gandi.main:Authenticator',
        ],
    },
)
