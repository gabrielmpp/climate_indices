from distutils.core import setup

setup(
  name = 'climIndices',         # How you named your package folder (MyLib)
  packages = ['climIndices'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Methods to download and format NOAA climate indices',   # Give a short description about your library
  author = 'Gabriel Perez',                   # Type in your name
  author_email = 'gabrielmpp2@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/gabrielmpp/climate_indices',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/gabrielmpp/climate_indices/archive/v0.2.tar.gz',    # I explain this later on
  keywords = ['climate', 'pandas'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3.6',
  ],
)
