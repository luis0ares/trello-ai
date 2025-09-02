from httpx import AsyncClient


async def test_create_board_with_success(async_client: AsyncClient):
    """Create a board with success."""
    response = await async_client.post('/boards', json={
        "name": 'Test Board',
        "position": 1
    })
    assert response.status_code == 201, response.json()
    data = response.json()
    assert data['name'] == 'Test Board'
    assert data['position'] == 1


async def test_get_all_boards_length_is_zero(async_client: AsyncClient):
    """Get all boards length is zero."""
    response = await async_client.get('/boards')
    assert response.status_code == 200, response.json()
    data = response.json()
    assert len(data) == 0


async def test_get_all_boards_with_todo(async_client: AsyncClient):
    """Get todo board."""
    # Arrange
    response = await async_client.post('/boards', json={
        "name": 'Todo',
        "position": 1
    })
    assert response.status_code == 201, response.json()
    todo = response.json()

    response = await async_client.get('/boards')
    assert response.status_code == 200, response.json()
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == todo['name']
    assert data[0]['position'] == todo['position']
