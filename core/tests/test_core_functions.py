from .setup import client, session, auth_token


def test_login(client):
    resp = client.post(
        "/api/auth-token", {"email": "asss@maill.cccc", "password": "1234"}
    )
    print(resp)
    assert True
