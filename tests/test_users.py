
import pytest
from app import schemas
from jose import jwt
from app.config import settings



def test_root(client):
    res = client.get('/')
    assert res.json().get('message') == "հոր ես պացալ, բալքամ վիրուսա!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello127@gmail.com", "password" : "password123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email =="hello127@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password" :  test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key,algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'Test1234', 404),
    ('sgh01@yopmail.com', 'password13', 404),
    ('wrongemail@gmail.com', 'wrongpassword', 404),
    (None, 'Test1234', 422),
    ('sgh01@yopmail.com', None, 422)
])

def test_incorrect_login(test_user  , client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})
    assert res.status_code == status_code