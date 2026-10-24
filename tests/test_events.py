import pytest
def test_create_event(client):
    response = client.post(
        '/events',
        json={
            "title": "Python Meetup",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data['id'] is not None
    assert data['title'] == 'Python Meetup'
    assert data['capacity'] == 30
    assert data['created_at'] is not None
    assert data['description'] == 'Встреча разработчиков'
    assert data['location'] == 'Amsterdam'


@pytest.mark.parametrize(
    'capacity',
    [0, -5]
)
def test_create_event_invalid_capacity(client, capacity):
    response = client.post(
        '/events',
        json={
            "title": "Python Meetup",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": capacity
        }
    )

    assert response.status_code == 422


def test_get_all_events(client):
    first_response = client.post(
        '/events',
        json={
            "title": "Python Meetup1",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert first_response.status_code == 201

    second_response = client.post(
        '/events',
        json={
            "title": "Python Meetup2",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert second_response.status_code == 201

    third_response = client.get(
        '/events'
    )

    assert third_response.status_code == 200

    data = third_response.json()

    assert any(event['title'] == 'Python Meetup1' for event in data)
    assert any(event['title'] == 'Python Meetup2' for event in data)

def test_get_event_by_id(client):
    response = client.post(
        '/events',
        json={
            "title": "Python Meetup1",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert response.status_code == 201

    data = response.json()
    event_id = data['id']

    second_response = client.get(
        f'/events/{event_id}'
    )

    assert second_response.status_code == 200

    second_data = second_response.json()

    assert second_data['title'] == data['title']
    assert second_data['id'] == event_id

def test_get_event_not_found(client):
    event_id = 99999

    response = client.get(
        f'/events/{event_id}'
    )

    assert response.status_code == 404

def test_delete_event(client):
    first_response = client.post(
        '/events',
        json={
            "title": "Python Meetup1",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert first_response.status_code == 201

    data = first_response.json()
    event_id = data['id']

    second_response = client.delete(
        f'/events/{event_id}'
    )

    assert second_response.status_code == 204

    third_response = client.get(
        f'/events/{event_id}'
    )

    assert third_response.status_code == 404


def test_delete_event_not_found(client):
    event_id = 99999
    response = client.delete(
        f'/events/{event_id}'
    )

    assert response.status_code == 404