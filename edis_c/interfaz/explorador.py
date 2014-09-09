# -*- coding: utf-8 -*-

from PyQt4.QtGui import (
    QListView,
    QWidget,
    QStandardItemModel,
    QStandardItem,
    QVBoxLayout
    )
from PyQt4.QtCore import (
    SIGNAL,
    QThread
    )

from edis_c.interfaz.contenedor_principal import contenedor_principal
from edis_c.nucleo import logger
log = logger.edisLogger('edis_c.interfaz.explorador')


class Explorador(QWidget):

    def __init__(self, parent=None):
        super(Explorador, self).__init__(parent)
        self._parent = parent
        self.model = None
        self.archivos = []

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.lista = QListView()
        vbox.addWidget(self.lista)
        self.hilo = ThreadArchivos(self)
        self.connect(self.hilo, SIGNAL("archivosRecibidos(QStringList)"),
            self.cargar_archivos)

    def cargar_archivos(self, archivos):
        archivos = list(archivos)
        if self.model is None:
            self.model = QStandardItemModel(self.lista)
            for i in archivos:
                item = QStandardItem(i.split('/')[-1])
                self.model.appendRow(item)
        self.lista.setModel(self.model)

    def cargar_archivo(self, archivo):
        item = QStandardItem(archivo.split('/')[-1])
        self.model.appendRow(item)

    def borrar_item(self, item):
        self.model.removeRow(item)

    def get_archivos(self):
        return contenedor_principal.ContenedorMain().get_archivos()

    def cambiar(self):
        #string = self.lista.currentIndex().data().toString()
        pass


class ThreadArchivos(QThread):

    def __init__(self, parent):
        super(ThreadArchivos, self).__init__()
        self.arc = []

    def run(self):
        try:
            cp = contenedor_principal.ContenedorMain()
            archivos = cp.tab.get_archivos_para_hilo()
            self.emit(SIGNAL("archivosRecibidos(QStringList)"),
                archivos)
        except:
            log.error('Error en ejecución de thread!')