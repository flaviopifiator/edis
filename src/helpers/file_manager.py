# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

""" Manejo de archivos """

import os

from PyQt4.QtCore import QFile, QTextStream, QIODevice

from src.helpers.exceptions import EdisIOException


def get_file_content(archivo):
    """ Lee el contenido de @archivo y lo retorna """

    try:
        with open(archivo, mode='rU') as filename:
            content = filename.read()
    except IOError as error:
        raise EdisIOException(error)
    return content


def get_file_size(archivo):
    """ Retorna el tamaño del archivo en bytes. """

    tam = QFile(archivo).size()
    return tam


def write_file(filename, content):
    """ Se escribe en el archivo, si el nombre no tiene extensión se agrega .c
    """

    ext = os.path.splitext(filename)[-1]
    if not ext:
        filename += '.c'
    _file = QFile(filename)
    if not _file.open(QIODevice.WriteOnly | QIODevice.Truncate):
        raise EdisIOException
    outfile = QTextStream(_file)
    outfile << content
    return filename
