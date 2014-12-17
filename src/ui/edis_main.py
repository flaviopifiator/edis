# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos Python
import os
import webbrowser

# Módulos QtGui
from PyQt4.QtGui import (
    QMainWindow,
    QIcon,
    QToolBar,
    )

# Módulos QtCore
from PyQt4.QtCore import (
    SIGNAL,
    Qt,
    QSize
    )

# Módulos EDIS
from src import ui
from src.helpers import configuraciones
from src.ui.contenedores.lateral import lateral_container
from src.ui.contenedores.output import contenedor_secundario
from src.ui.dialogos import dialogo_guardar_archivos


class EDIS(QMainWindow):
    """
    Esta clase es conocedora de todas las demás.

    """

    # Cada instancia de una clase  se guarda en éste diccionario
    __COMPONENTES = {}
    __MENUBAR = {}  # Nombre de los menus

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(ui.__nombre__)
        self.setMinimumSize(750, 500)
        # Maximizado
        self.showMaximized()
        # Secciones del menubar
        EDIS.menu_bar(0, self.trUtf8("&Archivo"))
        EDIS.menu_bar(1, self.trUtf8("&Editar"))
        EDIS.menu_bar(2, self.trUtf8("&Ver"))
        EDIS.menu_bar(3, self.trUtf8("&Buscar"))
        EDIS.menu_bar(4, self.trUtf8("&Herramientas"))
        EDIS.menu_bar(5, self.trUtf8("E&jecución"))
        EDIS.menu_bar(6, self.trUtf8("A&cerca de"))
        # Toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.setMovable(False)
        self.toolbar.setObjectName("toolbar")
        self.toolbar.setIconSize(QSize(28, 28))
        self.addToolBar(Qt.RightToolBarArea, self.toolbar)
        self.cargar_menu()
        # Barra de estado
        self.barra_de_estado = EDIS.componente("barra_de_estado")
        self.setStatusBar(self.barra_de_estado)
        # Widget central
        self.central = EDIS.componente("central")
        self.cargar_contenedores(self.central)
        self.setCentralWidget(self.central)

    @classmethod
    def cargar_componente(cls, nombre, instancia):
        """ Se guarda el nombre y la instancia de una clase """

        cls.__COMPONENTES[nombre] = instancia

    @classmethod
    def componente(cls, nombre):
        """ Devuelve la instancia de un componente """

        return cls.__COMPONENTES.get(nombre, None)

    @classmethod
    def menu_bar(cls, clave, nombre):
        """ Se guarda el nombre de cada menú """

        cls.__MENUBAR[clave] = nombre

    @classmethod
    def get_menu(cls, clave):
        """ Devuelve un diccionario con los menu """

        return cls.__MENUBAR.get(clave, None)

    def cargar_menu(self):
        #FIXME: Mejorar
        #FIXME: Separadores
        menu_bar = self.menuBar()
        menu_edis = self.componente("menu")
        principal = self.componente("principal")
        for i in range(7):
            menu = menu_bar.addMenu(self.get_menu(i))
            for accion in menu_edis.acciones:
                seccion = accion.seccion
                submenu = accion.submenu
                if seccion == i:
                    if submenu:
                        if isinstance(submenu, bool):
                            smenu = menu.addMenu(accion.nombre)
                        else:
                            qaccion = smenu.addAction(accion.nombre)
                    else:
                        qaccion = menu.addAction(accion.nombre)
                    if accion.nombre in configuraciones.ITEMS_TOOLBAR:
                        self.toolbar.addAction(qaccion)
                    if accion.atajo:
                        qaccion.setShortcut(accion.atajo)
                    icono = accion.icono
                    if icono:
                        qaccion.setIcon(QIcon(icono))
                    if accion.conexion:
                        if accion.conexion.split('.')[0] == 'edis':
                            funcion = getattr(self,
                                accion.conexion.split('.')[1], None)
                        else:
                            funcion = getattr(principal, accion.conexion, None)
                        # Es una función ?
                        if hasattr(funcion, '__call__'):
                            qaccion.triggered.connect(funcion)
                    if accion.separador:
                        menu.addSeparator()

    def cargar_contenedores(self, central):
        """ Carga los 3 contenedores (editor, lateral y output) """

        principal = EDIS.componente("principal")
        self.contenedor_editor = principal
        self.contenedor_output = contenedor_secundario.ContenedorOutput(self)
        self.contenedor_lateral = lateral_container.LateralContainer(self)

        # Agrego los contenedores al widget central
        central.agregar_contenedor_lateral(self.contenedor_lateral)
        central.agregar_contenedor_editor(self.contenedor_editor)
        central.agregar_contenedor_output(self.contenedor_output)

        self.connect(self.contenedor_editor,
                    SIGNAL("archivo_cambiado(QString)"),
                    self.__actualizar_estado)
        self.connect(self.contenedor_editor.stack,
                    SIGNAL("todo_cerrado()"),
                    self.todo_cerrado)
        self.connect(self.contenedor_editor,
                    SIGNAL("archivo_cambiado(QString)"),
                    self.__titulo_ventana)
        self.connect(self.contenedor_editor,
                    SIGNAL("archivo_modificado(bool)"),
                    self.__titulo_modificado)

    def __actualizar_estado(self, archivo):
        #FIXME: Hacer nuevo método para esto en barra de estado
        self.barra_de_estado.nombre_archivo.cambiar_texto(archivo)

    def todo_cerrado(self):
        self.setWindowTitle(ui.__nombre__)
        self.__actualizar_estado("")

    def __titulo_ventana(self, titulo):
        """ Cambia el título de la ventana (nombre_archivo - EDIS) """

        titulo = os.path.basename(titulo)
        self.setWindowTitle(titulo + ' - ' + ui.__nombre__)

    def __titulo_modificado(self, valor):
        """ Agrega (*) al título cuando el archivo es modificado """

        titulo_actual = self.windowTitle()
        if valor and not titulo_actual.startswith('*'):
            self.setWindowTitle('*' + titulo_actual)
        else:
            self.setWindowTitle(titulo_actual.split('*')[-1])

    def reportar_bug(self):
        webbrowser.open_new(ui.__reportar_bug__)

    def mostrar_ocultar_output(self):
        if self.contenedor_output.isVisible():
            self.contenedor_output.hide()
        else:
            self.contenedor_output.show()

    def mostrar_ocultar_lateral(self):
        if self.contenedor_lateral.isVisible():
            self.contenedor_lateral.hide()
        else:
            self.contenedor_lateral.show()

    def closeEvent(self, e):
        """
        Éste médoto es llamado automáticamente por Qt cuando se
        cierra la aplicación

        """

        principal = EDIS.componente("principal")
        if principal.check_archivos_sin_guardar():
            archivos_sin_guardar = principal.archivos_sin_guardar()  # lint:ok
            dialogo = dialogo_guardar_archivos.Dialogo(
                archivos_sin_guardar, principal)
            dialogo.exec_()
            if dialogo.ignorado():
                e.ignore()