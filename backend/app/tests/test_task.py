import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture(name="board_id")
async def create_board(async_client: AsyncClient):
    response = await async_client.post('/boards', json={
        "name": 'Todo',
        "position": 1
    })
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"
    board_id: str = response.json()["id"]
    yield board_id


async def test_create_task_with_success_without_description(
        async_client: AsyncClient, board_id: str):
    # Arrange & Act
    response = await async_client.post('/tasks', json={
        "board_id": board_id,
        "title": 'Test Task',
        "position": 1
    })

    # Assert
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"
    data = response.json()
    assert data['title'] == 'Test Task'
    assert data['description'] is None
    assert data['position'] == 1
    assert data['board_id'] == board_id


async def test_create_task_with_success_with_description(
        async_client: AsyncClient, board_id: str):
    # Arrange & Act
    response = await async_client.post('/tasks', json={
        "board_id": board_id,
        "title": 'Test Task',
        "description": 'Test Description',
        "position": 1
    })

    # Assert
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"
    data = response.json()
    assert data['title'] == 'Test Task'
    assert data['description'] == 'Test Description'
    assert data['position'] == 1
    assert data['board_id'] == board_id


async def test_get_board_with_tasks(
        async_client: AsyncClient, board_id: str):
    response = await async_client.post('/tasks', json={
        "board_id": board_id,
        "title": 'Test Task',
        "description": 'Test Description',
        "position": 1
    })
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"

    # Act
    response = await async_client.get('/boards')

    # Assert
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"
    data = response.json()
    assert len(data) == 1
    assert len(data[0]['tasks']) == 1
    assert data[0]['tasks'][0]['title'] == 'Test Task'
    assert data[0]['tasks'][0]['description'] == 'Test Description'
    assert data[0]['tasks'][0]['position'] == 1


async def test_update_task_with_success(
        async_client: AsyncClient, board_id: str):
    response = await async_client.post('/tasks', json={
        "board_id": board_id,
        "title": 'Test Task',
        "description": 'Test Description',
        "position": 1
    })
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"
    task_id = response.json()["id"]

    # Act
    response = await async_client.put(f'/tasks/{task_id}', json={
        "board_id": board_id,
        "title": 'Test Tasking',
        "description": None,
        "position": 5
    })

    # Assert
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"
    task_updated = response.json()
    assert task_updated['title'] == "Test Tasking"
    assert task_updated['description'] is None
    assert task_updated['position'] == 5


async def test_update_task_with_no_board_created(async_client: AsyncClient):
    # Act
    response = await async_client.put('/tasks/1', json={
        "board_id": "1",
        "title": 'Test Tasking',
        "description": None,
        "position": 5
    })

    # Assert
    assert response.status_code == 404, \
        f"Expected status code 404, but got {response.status_code}"
    assert response.json() == {'detail': 'Board not found'}


async def test_update_task_with_no_task(
        async_client: AsyncClient, board_id: str):
    # Act
    response = await async_client.put('/tasks/1', json={
        "board_id": board_id,
        "title": 'Test Tasking',
        "description": None,
        "position": 5
    })

    # Assert
    assert response.status_code == 404, \
        f"Expected status code 404, but got {response.status_code}"
    assert response.json() == {'detail': 'Task not found'}


async def test_delete_task_with_success(
        async_client: AsyncClient, board_id: str):
    # Arrange
    response = await async_client.post('/tasks', json={
        "board_id": board_id,
        "title": 'Test Tasking',
        "description": None,
        "position": 5
    })
    assert response.status_code == 201, \
        f"Expected status code 201, but got {response.status_code}"
    task_id = response.json()["id"]

    # Act
    response = await async_client.delete(f'/tasks/{task_id}')

    # Assert
    assert response.status_code == 204, \
        f"Expected status code 204, but got {response.status_code}"


async def test_delete_task_with_no_task(async_client: AsyncClient):
    # Act
    response = await async_client.delete('/tasks/1')

    # Assert
    assert response.status_code == 404, \
        f"Expected status code 404, but got {response.status_code}"
    assert response.json() == {'detail': 'Task not found'}
