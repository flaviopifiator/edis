# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import sys
from distutils.command.install import install
from distutils.core import setup

MODULES = [
    ('PyQt4', 'http://riverbankcomputing.co.uk/software/pyqt/intro'),
    ('PyQt4.Qsci', 'http://riverbankcomputing.co.uk/software/qscintilla/intro')
    ]

# Se verifica dependencias de módulos
for module, link in MODULES:
    try:
        _from = 'PyQt4' if module == 'PyQt4.Qsci' else ''
        __import__(module, fromlist=_from)
    except ImportError:
        print("El módulo %s no está instalado.\n%s para más info." %
              (module, link))
        sys.exit(1)

from src import ui


class CustomInstall(install):

    """ Clase de instalación personalizada.

    Copia todos los archivos en el directorio "PREFIX/share/Edis"
    """

    def run(self):
        install.run(self)

        for script in self.distribution.scripts:
            script_path = os.path.join(self.install_scripts,
                                       os.path.basename(script))
            with open(script_path, 'r') as f:
                content = f.read()
            content = content.replace('@ INSTALLED_BASE_DIR @',
                                      self._custom_data_dir)
            with open(script_path, 'w') as f:
                f.write(content)

            src_desktop = self.distribution.get_name() + '.desktop'
            src_desktop = src_desktop.lower()

            if not os.path.exists(self._custom_apps_dir):
                os.makedirs(self._custom_apps_dir)
            dst_desktop = os.path.join(self._custom_apps_dir, src_desktop)
            with open(src_desktop, 'r') as f:
                content = f.read()
            icon = os.path.join(self._custom_data_dir, 'src', 'images',
                                'icon.png')
            content = content.replace('@ INSTALLED_ICON @', icon)
            with open(dst_desktop, 'w') as f:
                f.write(content)

    def finalize_options(self):
        """ Después de la instalación """

        install.finalize_options(self)
        data_dir = os.path.join(self.prefix, "share",
                                self.distribution.get_name())
        apps_dir = os.path.join(self.prefix, "share", "applications")

        if self.root is None:
            build_dir = data_dir
        else:
            build_dir = os.path.join(self.root, data_dir[1:])
            apps_dir = os.path.join(self.root, apps_dir[1:])

        self.install_lib = build_dir
        self._custom_data_dir = data_dir
        self._custom_apps_dir = apps_dir


# Se compila la lista de paquetes
packages = []
for dir_path, dir_names, filenames in os.walk('src'):
    if '__pycache__' not in dir_path.split('/')[-1] and \
            '__init__.py' in filenames:
        package = dir_path.replace('/', '.')
        packages.append(package)

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: X11 Applications',
    'License :: OSI Approved :: GNU General Public License v3 or '
    'later (GPLv3+)',
    'Natural Language :: Spanish',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Text Editors :: Integrated Development Environments (IDE)',
    'Topic :: Utilities'
    ]

setup(
    name=ui.__edis__.title(),
    version=ui.__version__,
    description=ui.__description__,
    author=ui.__author__,
    author_email=ui.__email_author__,
    url=ui.__source_code__,
    license='GPLv3+',
    long_description=open('README.rst').read(),
    package_data={
        'src': ['extras/temas/*', 'images/icon.png', 'images/sources/logo.png',
                'ui/*.qml']
        },
    packages=packages,
    scripts=['bin/edis'],
    classifiers=classifiers,
    cmdclass={'install': CustomInstall},
    )
