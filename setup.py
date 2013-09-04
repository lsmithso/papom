from distutils.core import setup
setup(name='papom',
      version='0.0.1',
      packages = ['papom'],
      description='Python object model for Pulseaudio control',
      author='Les Smithson',
      author_email='lsmithso@hare.demon.co.uk',
      url='http://open-networks.co.uk',
      scripts = ['papomc'],
      provides=['papom'],
      requires = ['psutil'],


      )
