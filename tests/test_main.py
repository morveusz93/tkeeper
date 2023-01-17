import pytest


class TestUsersRest:
    @pytest.fixture(autouse=True)
    def set_up(self, client):
        self.test_user_data = {
            "email": "test@example.com", 
            "password": "chimichangas4life"
        }
        self.client = client

    def test_create_user_returns_200(self):
        response = self.client.post("/users/", json=self.test_user_data)

        assert response.status_code == 200

    def test_create_user_returns_400(self):
        self.client.post("/users/", json=self.test_user_data)
        response = self.client.post("/users/", json=self.test_user_data)

        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_create_user_returns_correct_data(self):
        response = self.client.post("/users/", json=self.test_user_data)

        response_data = response.json()
        assert response_data["email"] == "test@example.com"
        assert "id" in response_data

    def test_get_user_from_db(self):
        response_post = self.client.post("/users/", json=self.test_user_data)
        user_id = response_post.json()["id"]
        response_get = self.client.get(f"/users/{user_id}")

        response_get_data = response_get.json()
        assert response_get_data["email"] == "test@example.com"
