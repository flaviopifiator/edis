# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtGui import QApplication

import recursos


def edis():
    if not os.path.isdir(recursos.HOME_EDIS):
        os.mkdir(recursos.HOME_EDIS)

    import run
    app = QApplication([])
    run.correr_interfaz(app)