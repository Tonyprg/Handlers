import re
from functools import reduce
from typing import Union, Tuple

from .report import Report

class Handlers (Report):

    loglevels = ['DEBUG', 'INFO', 'WARNINGS', 'ERROR', 'CRITICAL']

    time_pattern     = r'(?P<time_pattern>\d+-\d+-\d+ \d+:\d+:\d+,\d*)'
    loglevel_pattern = r'(?P<loglevel_pattern>({})+)'.format(
        reduce(lambda a, b: a + ')|(' + b,
               loglevels))
    handler_pattern  = r'(?P<handler_pattern>/.*/)'
    all_pattern = rf'{time_pattern} {loglevel_pattern} django.request:[^/]+{handler_pattern}.*'

    @staticmethod
    def parse_django_request (request: str) -> Union[Tuple[str, str], None]:
        m = re.match(Handlers.all_pattern, request)
        if m:
            return m.group('loglevel_pattern'), \
                   m.group('handler_pattern')
        else:
            return None

    def __init__ (self) -> None:
        self.total_request:  int                       = 0
        self.table:          dict[str, dict[str, int]] = dict()
        self.total_loglevel: dict[str, int]            = {
            loglevel: 0
            for loglevel in Handlers.loglevels
        }

    def update_total_request (self, handler: str, loglevel: str) -> None:
         self.total_request += 1

    def update_table (self, handler: str, loglevel: str) -> None:
        if self.table.get(handler) is None:
            self.table[handler] = {
                lglvl: 0
                for lglvl in Handlers.loglevels
            }
        self.table[handler][loglevel] += 1

    def update_total_loglevel (self, handler: str, loglevel: str) -> None:
        self.total_loglevel[loglevel] += 1

    def update (self, request: str) -> None:
        match Handlers.parse_django_request(request):
            case loglevel, handler:
                self.update_total_request(handler, loglevel)
                self.update_table(handler, loglevel)
                self.update_total_loglevel(handler, loglevel)
            case None:
                pass

    def __str__ (self) -> str:

        # Соберем компоненты строк в список и далее используем join.
        # Так эффективнее
        res: list[list[str]] = []

        # Вычисляем размеры колонок
        cols = ['HANDLER'] + Handlers.loglevels
        colsz = {col: len(col) for col in cols}
        space = 2
        for handler in self.table:
            colsz['HANDLER'] = max(colsz['HANDLER'], len(handler))
            for loglevel, count in self.table[handler].items():
                colsz[loglevel] = max(colsz[loglevel], len(str(count)))
        for col in colsz:
            colsz[col] += space

        # Собираем шапку таблицы
        res.append([])
        for col in cols:
            res[-1].append(col.ljust(colsz[col]))

        #Собираем таблицу
        sorted_keys = list(self.table.keys())
        sorted_keys.sort()
        for handler in sorted_keys:
            res.append([])
            res[-1].append(handler.ljust(colsz['HANDLER']))
            for loglevel in Handlers.loglevels:
                count = self.table[handler][loglevel]
                res[-1].append(str(count).ljust(colsz[loglevel]))

        # Собираем сумму колонок - общее значение уровней логирования
        res.append([])
        res[-1].append(' ' * colsz['HANDLER'])
        for loglevel, count in self.total_loglevel.items():
            res[-1].append(str(count).ljust(colsz[loglevel]))

        union_res: str = '\n'.join([''.join(row) for row in res])

        return union_res
