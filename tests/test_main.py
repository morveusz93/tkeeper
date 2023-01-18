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

    def test_returns_404_when_user_does_not_exist(self):
        response_post = self.client.post("/users/", json=self.test_user_data)
        user_id = response_post.json()["id"]
        response_get = self.client.get(f"/users/{user_id + 1}")

        assert response_get.status_code == 404
        assert response_get.json()["detail"] == "User not found"

    def test_returns_empty_list_when_no_users(self):
        response_get = self.client.get(f"/users")

        assert response_get.status_code == 200
        assert response_get.json() == []

    def test_returns_multiple_users(self):
        self.client.post("/users/", json=self.test_user_data)
        self.test_user_data["email"] += "1"
        self.client.post("/users/", json=self.test_user_data)

        response_get = self.client.get(f"/users")

        assert response_get.status_code == 200
        assert len(response_get.json()) == 2


class TestSpidersRest:
    @pytest.fixture(autouse=True)
    def set_up(self, client):
        self.client = client
        test_user_data = {
            "email": "test@example.com", 
            "password": "chimichangas4life"
        }
        response = self.client.post("/users/", json=test_user_data)
        self.test_user = response.json()
        self.user_id = self.test_user["id"]
        self.test_spider_data = {
                "genus": "Brahypelma boehmei",
                "name": "Pusia",
                "molt": 5,
                "size": 12.2,
                "sex": "f",
                "extra_info": "Test test test",
        }

    def test_create_spider(self):
        response = self.client.post(f"/users/{self.user_id}/spiders", json={"genus": "Brahypelma boehmei"})

        assert response.status_code == 200
        
        response_data = response.json()
        
        assert response_data.get("id")
        assert response_data.get("sex") == 'n'

    def test_create_spider_with_all_fields(self):
        response = self.client.post(f"/users/{self.user_id}/spiders", json=self.test_spider_data)        
        response_data = response.json()
        
        assert response_data.get("id")
        assert response_data.get("sex") == 'f'
        assert response_data.get("molt") == 5
        assert response_data.get("size") == 12.2
        assert response_data.get("extra_info") == "Test test test"
        assert response_data.get("genus") == "Brahypelma boehmei"
        assert response_data.get("name") == "Pusia"
        

    def test_returns_error_when_no_genus_sent(self):
        self.test_spider_data.pop("genus")
        response = self.client.post(f"/users/{self.user_id}/spiders", json=self.test_spider_data)        
        assert response.status_code == 422

    def test_returns_epty_spiders_list(self):
        response = self.client.get("/spiders/")        
        assert response.status_code == 200
        assert response.json() == []


    def test_returns_multiple_spiders(self):
        response = self.client.post(f"/users/{self.user_id}/spiders", json=self.test_spider_data)        
        response = self.client.post(f"/users/{self.user_id}/spiders", json=self.test_spider_data)        
        response = self.client.post(f"/users/{self.user_id}/spiders", json=self.test_spider_data)        

        response = self.client.get("/spiders/")        
        assert response.status_code == 200
        assert len(response.json()) == 3
