try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

my_url = 'https://dreamtrack.ddns.net:3000/Dreamtrack/feh-browse'

config = {
	'description': 'A puny wallpaper browser in Python',
	'author': 'Adam J. Richardson',
	'url': my_url,
	'download_url': my_url,
	'author_email': 'fatman.uk@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['feh-browse'],
	'scripts': ['feh-browse'],
	'name': 'feh-browse'
}

setup(**config)

