import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '0.1.0'

#
# determine requirements
#
requirements = [
    "cliff",
    "boto"
]

try:
    import json  # noqa
except:
    try:
        import simplejson  # noqa
    except:
        requirements.append("simplejson >= 2.1.1")



#
# call setup
#
setup(
    name='dropkick',
    version=version,
    description="Swiss army knife for publishing to DreamObjects.",
    long_description=None,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet',
        'Topic :: Utilities'
    ],
    keywords='publish share cloud store archive',
    author='Jonathan LaCour',
    author_email='jonathan@cleverdevil.org',
    url='http://github.com/cleverdevil/dropkicker',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    scripts=[],
    zip_safe=False,
    install_requires=requirements,
    package_data={'dropkick': ['resources/reveal/*']},
    entry_points={
        'console_scripts': [
            'dropkick = dropkick.cli.main:main'
        ],
        'dropkick.cli': [
            'config = dropkick.cli.config:Configure',
            'document = dropkick.cli.document:PublishDocument',
            'presentation = dropkick.cli.presentation:PublishPresentation',
            'share = dropkick.cli.share:ShareFiles'
        ],
    },
)
