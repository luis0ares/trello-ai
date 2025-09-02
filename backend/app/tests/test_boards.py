from httpx import AsyncClient


async def test_create_board_with_success(async_client: AsyncClient):
    # Arrange & Act
    response = await async_client.post('/boards', json={
        "name": 'Test Board',
        "position": 1
    })

    # Assert
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"
    data = response.json()
    assert data['name'] == 'Test Board'
    assert data['position'] == 1


async def test_get_all_boards_length_is_zero(async_client: AsyncClient):
    # Act
    response = await async_client.get('/boards')

    # Assert
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"
    data = response.json()
    assert len(data) == 0


async def test_get_all_boards_with_todo(async_client: AsyncClient):
    # Arrange
    response = await async_client.post('/boards', json={
        "name": 'Todo',
        "position": 1
    })
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"
    todo = response.json()

    # Act
    response = await async_client.get('/boards')

    # Assert
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert len(data) == 1
    assert len(data[0]['tasks']) == 0
    assert data[0]['name'] == todo['name']
    assert data[0]['position'] == todo['position']


async def test_update_board_with_success(async_client: AsyncClient):
    # Arrange
    response = await async_client.post('/boards', json={
        "name": 'Todo',
        "position": 1
    })
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"
    board_id = response.json()["id"]

    # Act
    response = await async_client.put(f'/boards/{board_id}', json={
        "name": 'Todoing',
        "position": 5
    })

    # Assert
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"
    board_updated = response.json()
    assert board_updated['name'] == "Todoing"
    assert board_updated['position'] == 5


async def test_update_board_with_no_board(async_client: AsyncClient):
    # Act
    response = await async_client.put('/boards/1', json={
        "name": 'Todoing',
        "position": 5
    })

    # Assert
    assert response.status_code == 404, \
        f"Expected status code 404, but got {response.status_code}"
    assert response.json() == {'detail': 'Board not found'}


async def test_delete_board_with_success(async_client: AsyncClient):
    # Arrange
    response = await async_client.post('/boards', json={
        "name": 'Todo',
        "position": 1
    })
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"
    board_id = response.json()["id"]

    # Act
    response = await async_client.delete(f'/boards/{board_id}')

    # Assert
    assert response.status_code == 204, \
        f"Expected status code 204, but got {response.status_code}"


async def test_delete_board_with_no_board(async_client: AsyncClient):
    # Act
    response = await async_client.delete('/boards/1')

    # Assert
    assert response.status_code == 404, \
        f"Expected status code 404, but got {response.status_code}"
    assert response.json() == {'detail': 'Board not found'}
