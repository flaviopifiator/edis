# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QKeySequence

from PyQt4.QtCore import Qt


# Atajos
SHORTCUTS = {
    # Archivo
    "new": QKeySequence(Qt.CTRL + Qt.Key_N),
    "open": QKeySequence(Qt.CTRL + Qt.Key_O),
    "reload": QKeySequence(Qt.Key_F5),
    "save": QKeySequence(Qt.CTRL + Qt.Key_S),
    "close": QKeySequence(Qt.CTRL + Qt.Key_W),
    "properties": QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_P),
    "exit": QKeySequence(Qt.CTRL + Qt.Key_Q),
    # Editar
    "undo": QKeySequence(Qt.CTRL + Qt.Key_Z),
    "redo": QKeySequence(Qt.CTRL + Qt.Key_Y),
    "cut": QKeySequence(Qt.CTRL + Qt.Key_X),
    "copy": QKeySequence(Qt.CTRL + Qt.Key_C),
    "paste": QKeySequence(Qt.CTRL + Qt.Key_V),
    "select": QKeySequence(Qt.CTRL + Qt.Key_A),
    "indent": QKeySequence(Qt.Key_Tab),
    "unindent": QKeySequence(Qt.SHIFT + Qt.Key_Tab),
    "up": QKeySequence(Qt.ALT + Qt.Key_Up),
    "down": QKeySequence(Qt.ALT + Qt.Key_Down),
    "comment": QKeySequence(Qt.CTRL + Qt.Key_G),
    "uncomment": QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_G),
    "title": QKeySequence(Qt.CTRL + Qt.Key_T),
    "delete": QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_X),
    "duplicate": QKeySequence(Qt.ALT + Qt.Key_D),
    "preferences": QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_P),
    # Ver
    "fullscreen": QKeySequence(Qt.CTRL + Qt.Key_F11),
    "hide-all": QKeySequence(Qt.Key_F11),
    "hide-toolbar": QKeySequence(Qt.Key_F8),
    "hide-output": QKeySequence(Qt.Key_F7),
    "zoom-in": QKeySequence(Qt.CTRL + Qt.Key_Plus),
    "zoom-out": QKeySequence(Qt.CTRL + Qt.Key_Minus),
    "normal-font-size": QKeySequence(Qt.CTRL + Qt.Key_0),
    "show-selector": QKeySequence(Qt.CTRL + Qt.Key_M),
    # Código
    "build": QKeySequence(Qt.CTRL + Qt.Key_F5),
    "run": QKeySequence(Qt.CTRL + Qt.Key_F6),
    "build-run": QKeySequence(Qt.CTRL + Qt.Key_F10),
    "stop": QKeySequence(Qt.CTRL + Qt.Key_B),
    # Buscar
    "find": QKeySequence(Qt.CTRL + Qt.Key_F),
    "find-replace": QKeySequence(Qt.CTRL + Qt.Key_H),
    "go": QKeySequence(Qt.CTRL + Qt.Key_J)
    }
