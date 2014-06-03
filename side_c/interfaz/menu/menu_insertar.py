#-*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import QObject
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from side_c.interfaz.editor import acciones_
from side_c import recursos


class MenuInsertar(QObject):

    def __init__(self, menu_insertar, toolbar, ide):
        super(MenuInsertar, self).__init__()

        self.ide = ide

        accionTitulo = menu_insertar.addAction(
            QIcon(recursos.ICONOS['titulo']), self.trUtf8("Título"))
        accionTitulo.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_C)
        accionSeparador = menu_insertar.addAction(
            QIcon(recursos.ICONOS['linea']), self.trUtf8("Separador"))
        accionSeparador.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_S)

        self.connect(accionSeparador, SIGNAL("triggered()"),
            self.insertar_separador)
        self.connect(accionTitulo, SIGNAL("triggered()"),
            self.insertar_titulo)

        self.items_toolbar = {
            "linea": accionSeparador,
            "titulo": accionTitulo
            }

    def insertar_separador(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW and editorW.hasFocus():
            acciones_.insertar_linea(editorW)

    def insertar_titulo(self):
        editorW = self.ide.contenedor_principal.devolver_editor_actual()
        if editorW and editorW.hasFocus():
            acciones_.insertar_titulo(editorW)