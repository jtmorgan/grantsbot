try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'grantsbot/matching',
    'author': 'Frances Hocutt',
    'url': 'https://github.com/fhocutt/grantsbot-matching',
    'download_url': '',
    'author_email': 'fhocutt+matchbot@wikimedia.org',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['matching'],
    'scripts': [],
    'name': 'GrantsBot/matching'
}

setup(**config)
