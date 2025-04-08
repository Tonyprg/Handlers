from report.handlers import Handlers

def test_parse_django_request () -> None:

    arg = [
        '2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]',
        '2025-03-28 12:21:51,000 WARNINGS django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]',
        '2025-03-28 12:24:19,000 DEBUG django.db.backends: (0.13) SELECT * FROM \'orders\' WHERE id = 60;',
    ]

    res = [
        ('INFO', '/api/v1/reviews/'),
        ('WARNINGS', '/admin/dashboard/'),
        None
    ]

    for i in range(len(arg)):
        assert(Handlers.parse_django_request(arg[i]) == res[i])

def test_table () -> None:

    hnd = Handlers()
    hnd.update('2025-03-28 12:44:46,000 INFO django.request: GET /one/ 204 OK [192.168.1.59]')
    hnd.update('2025-03-28 12:21:51,000 WARNINGS django.request: GET /one/ 200 OK [192.168.1.68]')
    hnd.update('2025-03-28 12:21:51,000 WARNINGS django.request: GET /two/ 200 OK [192.168.1.68]')

    assert(hnd.table['/one/']['DEBUG']    == 0)
    assert(hnd.table['/one/']['INFO']     == 1)
    assert(hnd.table['/one/']['WARNINGS'] == 1)
    assert(hnd.table['/one/']['ERROR']    == 0)
    assert(hnd.table['/one/']['CRITICAL'] == 0)

    assert(hnd.table['/two/']['DEBUG']    == 0)
    assert(hnd.table['/two/']['INFO']     == 0)
    assert(hnd.table['/two/']['WARNINGS'] == 1)
    assert(hnd.table['/two/']['ERROR']    == 0)
    assert(hnd.table['/two/']['CRITICAL'] == 0)
