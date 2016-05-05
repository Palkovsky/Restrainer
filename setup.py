from distutils.core import setup
setup(
  name = 'restrainer',
  packages = ['restrainer', 'restrainer/constraints'], # this must be the same as the name above
  version = '1.2',
  description = 'Lightweight, flexible validation library.',
  author = 'Dawid Macek',
  author_email = 'dawidmacek42@gmail.com',
  url = 'https://github.com/Palkovsky/Strainer', # use the URL to the github repo
  download_url = 'https://github.com/Palkovsky/Strainer/tree/master/strainer', # I'll explain this in a second
  keywords = ['validation', 'library', 'rest api'], # arbitrary keywords
  classifiers = [],
)