# setup.py for GSOF-Cockpit
#
# Windows installer:
#   "python setup.py bdist_wininst"
#
# Direct install (all systems):
#   "python setup.py install"
#
# For Python 3.x use the corresponding Python executable,
# e.g. "python3 setup.py ..."

#from setuptools import setup
from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
      name='GSOF-Pygame-Cockpit-Instruments',
      version='0.1',
      description='GSOF Cockpit-Instruments under Pygame',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
      ],
      platforms = 'any',
      keywords='Cockpit',
      url='https://github.com/mrGSOF/GSOF_Cockpit',
      author='Guy Soffer',
      author_email='gsoffer@yahoo.com',
      license='MIT',
      packages=['GSOF_Cockpit'],
      package_dir={'GSOF_Cockpit': 'GSOF_Cockpit'},
      package_data={'GSOF_Cockpit': ['Aerospace/*.*',
                                     'Automotive/*.*',
                                     'Generic/*.*',
                                     'Wireframe3D/*.*',
                                     'resources/*.*',
                                     'skin/*.*',
                                     'objects/*.*',
                                     'Examples/*.*',
                                     ]},
#     #include_package_data=True,
       install_requires=['markdown',],
#      test_suite='nose.collector',
#      tests_require=['nose', 'nose-cover3'],
#      entry_points={
#          'console_scripts': ['funniest-joke=funniest.command_line:main'],
#     },
#      zip_safe=False
)
