from core.tests.setup import session, client, auth_token


def test_me(client, auth_token):
    response = client.get(
        "api/v1/me", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


def test_create_user(client, auth_token):
    response = client.post(
        "/api/v1/users",
        json={
            "name": "John Doe",
            "email": "johndoe@mail.com",
            "password": "1234",
            "confirm_password": "1234",
        },
    )
    assert response.status_code == 201
    assert response.json()["data"]["email"] == "johndoe@mail.com"
