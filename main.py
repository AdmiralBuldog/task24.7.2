import requests
import unittest


class TestPetFriendsAPI(unittest.TestCase):
    BASE_URL = "https://petfriends.skillfactory.ru"

    def setUp(self):
        self.api_key = "312ff7e56ac4bf3c6d7a87419d4cfc76dd513c4b1d5b6d470ff51195"

    # Позитивный тест. Проверка создания питомца с корректными данными
    def test_create_pet_simple_positive(self):
        headers = {
            "auth_key": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "name": "TestPet",
            "animal_type": "Dog",
            "age": "5"
        }
        response = requests.post(f"{self.BASE_URL}/api/create_pet_simple", headers=headers, data=data)
        print(response.text)  # Для вывода ответа сервера
        self.assertEqual(response.status_code, 200)

        print(response.text)

        self.assertEqual(response.status_code, 200)

    # Негативные тесты

    def test_large_values(self):
        # Передача слишком больших значений в параметрах
        response = requests.post(f"{self.BASE_URL}/create_pet_simple",
                                 headers={"auth_key": self.api_key},
                                 data={"name": "TestPet" * 100, "animal_type": "Dog" * 100, "age": "5" * 100})
        self.assertNotEqual(response.status_code, 200)

    def test_missing_parameters(self):
        # Отсутствие необходимых параметров
        response = requests.post(f"{self.BASE_URL}/create_pet_simple",
                                 headers={"auth_key": self.api_key},
                                 data={"name": "TestPet"})
        self.assertNotEqual(response.status_code, 200)

    def test_wrong_auth_key(self):
        # Передача неверного ключа авторизации
        response = requests.post(f"{self.BASE_URL}/create_pet_simple",
                                 headers={"auth_key": "wrong_key"},
                                 data={"name": "TestPet", "animal_type": "Dog", "age": "5"})
        self.assertNotEqual(response.status_code, 200)

    def test_wrong_data_format(self):
        # Передача неверного формата данных
        response = requests.post(f"{self.BASE_URL}/create_pet_simple",
                                 headers={"auth_key": self.api_key},
                                 data={"name": "TestPet", "animal_type": "Dog", "age": "five"})
        self.assertNotEqual(response.status_code, 200)

    def test_access_without_auth(self):
        # Попытка доступа к ресурсам без авторизации
        response = requests.post(f"{self.BASE_URL}/create_pet_simple",
                                 data={"name": "TestPet", "animal_type": "Dog", "age": "5"})
        self.assertNotEqual(response.status_code, 200)

    def test_duplicate_data(self):
        # Попытка создания ресурса с уже существующими уникальными данными
        requests.post(f"{self.BASE_URL}/create_pet_simple",
                      headers={"auth_key": self.api_key},
                      data={"name": "DuplicatePet", "animal_type": "Dog", "age": "5"})
        response = requests.post(f"{self.BASE_URL}/create_pet_simple",
                                 headers={"auth_key": self.api_key},
                                 data={"name": "DuplicatePet", "animal_type": "Dog", "age": "5"})
        self.assertNotEqual(response.status_code, 200)

    def test_special_characters(self):
        # Передача специальных символов в параметрах
        response = requests.post(f"{self.BASE_URL}/create_pet_simple",
                                 headers={"auth_key": self.api_key},
                                 data={"name": "<script>alert('Test')</script>", "animal_type": "Dog", "age": "5"})
        self.assertNotEqual(response.status_code, 200)

    def test_out_of_bounds_data(self):
        # Передача данных, которые выходят за пределы допустимых значений
        response = requests.post(f"{self.BASE_URL}/create_pet_simple",
                                 headers={"auth_key": self.api_key},
                                 data={"name": "TestPet", "animal_type": "Dog", "age": "-5"})
        self.assertNotEqual(response.status_code, 200)

    def test_nonexistent_resource(self):
        # Попытка удаления или изменения несуществующего ресурса
        response = requests.delete(f"{self.BASE_URL}/pets/999999",
                                   headers={"auth_key": self.api_key})
        self.assertNotEqual(response.status_code, 200)

    def test_no_permission(self):
        # Попытка выполнения действий, на которые у пользователя нет прав
        # Для этого теста предполагается, что у пользователя нет прав на удаление питомца с ID 1
        response = requests.delete(f"{self.BASE_URL}/pets/1",
                                   headers={"auth_key": self.api_key})
        self.assertNotEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
