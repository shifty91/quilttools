# SPDX-License-Identifier: GPL2.0
# Copyright Benedikt Spranger <b.spranger@linutronix.de>

"""
quilttools: package information and setup
"""

from distutils.command.build import build
from re import sub
from time import time
from setuptools import setup, find_packages

from git import InvalidGitRepositoryError, Repo
from sphinx.setup_command import BuildDoc

from quilttoolsversion import QUILTTOOLSVERSION as version

NAME = 'quilttools'

CMDCLASS = {'build_sphinx': BuildDoc}

try:
    repo = Repo()
    assert not repo.bare
    gitversion = repo.git.describe('--tags', '--dirty', '--broken')
    gitversion = sub(r'^\D*', '', gitversion, count=1)
except InvalidGitRepositoryError:
    gitversion = ''

if gitversion.__contains__('-'):
    version = gitversion.split('-')[0]
    release = version + '.dev%d'%time()
else:
    release = version

print("Package Information:")
print("name   : %s"%NAME)
print("version: %s"%version)
print("release: %s"%release)
print("git    : %s"%gitversion)

with open("README.md", "r") as fh:
    long_description = fh.read()

class BuildExtras(build):
    """ Override distutil build command to build man pages """
    def run(self):
        super().run()
        cmd_obj = self.distribution.get_command_obj('build_sphinx')
        cmd_obj.builder = "man"
        self.run_command('build_sphinx')

CMDCLASS = {'build': BuildExtras, 'build_sphinx': BuildDoc}
DATA_FILES = [("share/doc/" + NAME + "/examples",
               ["Documentation/examples/.mb2q.yaml"]),
              ("share/man/man1/", ["build/sphinx/man/mb2q.1"])]
PACKAGE_DATA = {"": ["*.rst", "*.txt", "LICENSES/*", "Documentation/conf.py"]}

setup(
    name=NAME,
    version=release,
    author="Thomas Gleixner",
    author_email="tglx@linutronix.de",
    license="GPL2.0",
    description="A small but powerful collection of quilt helper tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.kernel.org/pub/scm/linux/kernel/git/tglx/quilttools.git",
    packages=find_packages(),
    package_data=PACKAGE_DATA,
    data_files=DATA_FILES,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Email :: Filters",
        "Topic :: Software Development",
    ],
    platforms=['any'],
    python_requires='>=3.6',
    scripts=['mb2q'],
    install_requires=['pyyaml', 'notmutch'],
    cmdclass=CMDCLASS,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', NAME),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'Documentation')}},
)
