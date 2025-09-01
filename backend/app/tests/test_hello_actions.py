async def test_root_not_found(async_client):
    response = await async_client.get('/')
    assert response.status_code == 404, response.json()
