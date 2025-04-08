import sys

from report import Report
from report import Handlers

def make_report (file_names: list[str], report_name: str) -> None:
    try:
        report = reports[report_name]
        for name in file_names:
            with open(name, 'r') as file:
                for request in file:
                    report.update(request)
        print(f'REPORT: {report_name}\n')
        print(report)
        print()

    except FileNotFoundError as e:
        print(f'Файла с именем {e} не существует\n')

    except KeyError as e:
        print(f'Отчет с именем {e} не предусмотрен.\n')


# Здесь добавляются отчеты.
# Отчет должен содержать методы update и __str__
reports: dict[str, Report]  = {
    'handlers': Handlers()
}


if __name__ == '__main__':

    file_names:   list[str] = []
    report_names: list[str] = []

    to_extend = file_names
    for arg in sys.argv:
        if arg == '--report':
            to_extend = report_names
            continue
        to_extend.append(arg)

    for report_name in report_names:
        make_report(file_names, report_name)
