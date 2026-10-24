def test_create_registration(client):
    first_response = client.post(
        '/events',
        json={
            "title": "Python Meetup",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert first_response.status_code == 201

    event_id = first_response.json()['id']

    second_response = client.post(
        f'/events/{event_id}/registrations',
        json={
            'attendee_name': 'Alex',
            'attendee_email': 'user@gmail.com'
        }
    )

    assert second_response.status_code == 201

    data = second_response.json()

    assert data['attendee_name'] == 'Alex'
    assert data['attendee_email'] == 'user@gmail.com'



def test_create_registration_event_not_found(client):
    event_id = 99999

    response = client.post(
        f'/events/{event_id}/registrations',
        json={
            'attendee_name': 'Alex',
            'attendee_email': 'user@gmail.com',
        }
    )

    assert response.status_code == 404


def test_create_registration_duplicate_email(client):
    first_response = client.post(
        '/events',
        json={
            "title": "Python Meetup",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert first_response.status_code == 201

    event_id = first_response.json()['id']

    second_response = client.post(
        f'/events/{event_id}/registrations',
        json={
            'attendee_name': 'Alex',
            'attendee_email': 'user@gmail.com'
        }
    )

    assert second_response.status_code == 201

    third_response = client.post(
        f'/events/{event_id}/registrations',
        json={
            'attendee_name': 'Alex',
            'attendee_email': 'user@gmail.com'
        }
    )

    assert third_response.status_code == 409


def test_create_registration_same_email_different_events(client):
    first_response = client.post(
        '/events',
        json={
            "title": "Python Meetup",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert first_response.status_code == 201

    event_id = first_response.json()['id']

    second_response = client.post(
        f'/events/{event_id}/registrations',
        json={
            'attendee_name': 'Alex',
            'attendee_email': 'user@gmail.com'
        }
    )

    assert second_response.status_code == 201

    third_response = client.post(
        '/events',
        json={
            "title": "Python Meetup",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert third_response.status_code == 201

    event_id = third_response.json()['id']

    fourth_response = client.post(
        f'/events/{event_id}/registrations',
        json={
            'attendee_name': 'Alex',
            'attendee_email': 'user@gmail.com'
        }
    )

    assert fourth_response.status_code == 201


def test_create_registration_event_full(client):
    first_response = client.post(
        '/events',
        json={
            "title": "Python Meetup",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 1
        }
    )

    assert first_response.status_code == 201

    event_id = first_response.json()['id']

    second_response = client.post(
        f'/events/{event_id}/registrations',
        json={
            'attendee_name': 'Alex',
            'attendee_email': 'user1@gmail.com'
        }
    )

    assert second_response.status_code == 201


    third_response = client.post(
        f'/events/{event_id}/registrations',
        json={
            'attendee_name': 'Alex',
            'attendee_email': 'user2@gmail.com'
        }
    )

    assert third_response.status_code == 409



def test_get_registration_stats(client):
    first_response = client.post(
        '/events',
        json={
            "title": "Python Meetup",
            "description": "Встреча разработчиков",
            "location": "Amsterdam",
            "starts_at": "2027-01-15T18:00:00",
            "capacity": 30
        }
    )

    assert first_response.status_code == 201

    event_id = first_response.json()['id']

    second_response = client.post(
        f'/events/{event_id}/registrations',
        json={
            'attendee_name': 'Alex',
            'attendee_email': 'user1@gmail.com'
        }
    )

    assert second_response.status_code == 201

    third_response = client.get(
        f'/events/{event_id}/registrations/stats'
    )

    assert third_response.status_code == 200

    data = third_response.json()

    assert data['registered_count'] == 1
    assert data['event_id'] == event_id
    assert data['capacity'] == 30
    assert data['available_places'] == 29


def test_get_registration_stats_event_not_found(client):
    event_id = 99999

    response = client.get(
        f'/events/{event_id}/registrations/stats'
    )

    assert response.status_code == 404

