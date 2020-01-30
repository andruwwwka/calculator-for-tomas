"""Тесты для http ресурсов."""


async def test_index_view(tables_and_data, client):
    """Доступность главной страницы."""
    resp = await client.get('/')
    assert resp.status == 200


async def test_calculate_view_without_parameters(tables_and_data, client):
    """Метод вычисления отдает ошибку при отсутствии параметров."""
    resp = await client.get('/api/calculate/')
    resp_json = await resp.json()
    assert resp.status == 400
    assert all([field in resp_json for field in {'state', 'count', 'price'}])


async def test_calculate_view_with_invalid_parameters(tables_and_data, client):
    """Метод вычисления выдает ошибку, если хотя бы один из параметров невалидный."""
    resp = await client.get('/api/calculate/', params={'price': 'a', 'count': 250, 'state': 'AR'})
    resp_json = await resp.json()
    assert 'price' in resp_json
    assert resp_json['price'] == ['Not a valid number.']
    assert resp.status == 400


async def test_raise_not_exists_state(tables_and_data, client):
    """Метод вычисления выдает 404 код, если поступает запрос со штатом, для которого нет записи с налогом."""
    resp = await client.get('/api/calculate/', params={'price': '20.0', 'count': 250, 'state': 'GA'})
    assert resp.status == 404


async def test_calculate_rate(tables_and_data, client):
    """Позитивный кейс, когда происходит вычисление суммы."""
    resp = await client.get('/api/calculate/', params={'price': '20.0', 'count': 5, 'state': 'AR'})
    resp_json = await resp.json()
    assert resp.status == 200
    assert resp_json == {'total_amount': 100.42, 'amount_with_discount': 95.0}
