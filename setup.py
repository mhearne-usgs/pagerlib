from distutils.core import setup

setup(name='pagerlib',
      version='0.1dev',
      description='USGS PAGER generic library functionality',
      author='Mike Hearne',
      author_email='mhearne@usgs.gov',
      url='',
      packages=['pagerutil','pagerio','pagermap'],
      install_requires=['numpy', 'matplotlib', 'scipy'],
      scripts = ['getcomcat.py'],
)
