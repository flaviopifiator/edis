# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import re

"""
Analizador de estilo de código para C.
C es un lenguaje que no obliga a tener el código organizado para funcionar,
podemos tener un programa escrito en una sola línea y funcionaría, pero esto es
un problema ya que el código se hace ilegible y difícil de mantener.
Éste analizador captura los errores más comunes.
"""

# Máximo número de caracteres en una línea
MAX_LINE_LENGTH = 79
REGEX_COMMENT_LINE = re.compile("^\s*\/\*.*\*\/\s*$")
REGEX_OPERATOR_SPACE = re.compile("(\w\s?(\+|\-|\*|\<|\>|\=)\w)" +
                                  "|(\w(\=\=|\<\=|\>\=)\w)")
# Mensajes
M_MAX_LINE_LENGTH = "%s:La línea supera los %s caracteres."
M_OPERATOR_SPACE = "%s:Poner espacio alrededor de operadores."


class EChecker(object):

    def __init__(self, source_list):
        self._source = source_list
        self._line_number = 1
        self._results = []

    def _check_max_line_length(self, line):
        """ La línea no debe superar los 79 caracteres """

        if len(line) > MAX_LINE_LENGTH:
            self._results.append(M_MAX_LINE_LENGTH % (self._line_number,
                                 MAX_LINE_LENGTH))

    def _check_operator_space(self, line):
        """ Verifica si hay espacios entre operadores.

        /* MAL */
        int i;
        i = i+2;

        /* BIEN */
        int i;
        i = i + 2;

        """
        if REGEX_OPERATOR_SPACE.search(line) and not line.startswith('#'):
            if not REGEX_COMMENT_LINE.search(line):
                self._results.append(M_OPERATOR_SPACE % self._line_number)

    def run_all_checks(self):
        for line in self._source:
            # Checkers
            self._check_max_line_length(line)
            self._check_operator_space(line)
            self._line_number += 1
        return self._results


def run_checker(source):
    lines = [line for line in source.splitlines()]
    return EChecker(lines).run_all_checks()