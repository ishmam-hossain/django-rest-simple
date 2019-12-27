from rest_framework.test import APITestCase
from rest_framework import status


class ValuesAPITestCase(APITestCase):
    API_PATH = "/api/values/"

    def test_get_ok(self):
        response = self.client.get(self.API_PATH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_keys_ok(self):
        response = self.client.get(f"{self.API_PATH}?keys=key1,key2,key3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_ok(self):
        data = {"test": "ok"}
        response = self.client.post(self.API_PATH, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_ok(self):
        data = {"test": "patch"}
        response = self.client.patch(self.API_PATH, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_patch_empty_json_data(self):
        data = {}
        response = self.client.post(self.API_PATH, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(self.API_PATH, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

