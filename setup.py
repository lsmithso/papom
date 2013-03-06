from distutils.core import setup
setup(name='stfu',
      version='0.0.1',
      packages = ['stfu'],
      description='Manage pulseaudio sinks, sources and clients in useful ways',
      author='Les Smithson',
      author_email='lsmithso@hare.demon.co.uk',
      url='http://open-networks.co.uk',
      scripts = ['stfuc'],
      provides=['stfu'],


      )
