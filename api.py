import requests
from requests.exceptions import HTTPError


class PetFriendsAPI:
    def __init__(self):
        self.BASE_URL = "https://petfriends.skillfactory.ru"

    def adopt_pet(self, pet_id, headers):
        """Процесс усыновления/приёма питомца пользователем."""
        url = f"{self.BASE_URL}/api/pets/{pet_id}/adopt"
        response = requests.post(url, headers=headers)

        # Проверка на статус код 200 и вызов исключения HTTPError при неудаче
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            raise HTTPError(f"HTTP error occurred: {http_err}")

        return response.json()

    def search_pets(self, headers, **kwargs):
        """Поиск питомцев по различным критериям."""
        url = f"{self.BASE_URL}/api/pets/search"
        response = requests.get(url, headers=headers, params=kwargs)

        # Проверка на статус код 200 и вызов исключения HTTPError при неудаче
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            raise HTTPError(f"HTTP error occurred: {http_err}")

        return response.json()
