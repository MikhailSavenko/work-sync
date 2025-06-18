from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from tests.factories import UserFactory, TeamFactory
from account.models import Worker, Team

from django.urls import reverse


class TeamApiTestCase(APITestCase):

    ONE = 1

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Создадим admin_team Worker
        cls.user0 = UserFactory()
        cls.worker0 = cls.user0.worker
        cls.worker0.role = Worker.Role.ADMIN_TEAM
        cls.worker0.save()

        # Создадим normal Worker
        cls.user1 = UserFactory()
        cls.worker1 = cls.user1.worker

        # Создадим admin_team Worker 2
        cls.user2 = UserFactory()
        cls.worker2 = cls.user2.worker
        cls.worker2.role = Worker.Role.ADMIN_TEAM
        cls.worker2.save()

        # Создадим manager Worker
        cls.user3 = UserFactory()
        cls.worker3 = cls.user3.worker
        cls.worker3.role = Worker.Role.MANAGER
        cls.worker3.save()
        
        cls.data_team = {
            "title": "Test Team",
            "description": "Test descript =)",
            "workers": [
              cls.worker0.id
            ]
        }
        cls.update_data_team = {
            "title": "Test Team Update",
            "description": "Test descript Update =)",
            "workers": [
              cls.worker0.id
            ]
        }

        cls.team = TeamFactory(creator=cls.worker0)
        cls.team2 = TeamFactory(creator=cls.worker0)
        cls.worker1.team = cls.team2
        cls.worker1.save()
 
    def test_admin_can_create_team(self):
        self.client.force_authenticate(user=self.user0)
        response = self.client.post(reverse("account:teams-list"), data=self.data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.data_team["title"])
        self.assertEqual(response.data["description"], self.data_team["description"])
    
    def test_admin_can_update_his_team(self):
        self.client.force_authenticate(user=self.user0)
        response = self.client.put(reverse("account:teams-detail", kwargs={"pk": self.team.id}), data=self.update_data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.update_data_team["title"])
        self.assertEqual(response.data["description"], self.update_data_team["description"])
    
    def test_admin_can_get_list_team(self):
        self.client.force_authenticate(user=self.user0)
        response = self.client.get(reverse("account:teams-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.team.title)

    def test_admin_can_get_detail_team(self):
        self.client.force_authenticate(user=self.user0)
        response = self.client.get(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.team.title)
    
    def test_admin_can_delete_his_team(self):
        team_count = Team.objects.count()
        self.client.force_authenticate(user=self.user0)
        response = self.client.delete(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(team_count - self.ONE, Team.objects.count())
    
    def test_admin_cant_delete_foreign_team(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_cant_create_team(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse("account:teams-list"), data=self.data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_cant_update_foreign_team(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(reverse("account:teams-detail", kwargs={"pk": self.team.id}), data=self.update_data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_normal_can_get_list_team(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse("account:teams-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.team.title)

    def test_normal_can_get_detail_team(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.team.title)
    
    def test_normal_cant_delete_foreign_team(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_manager_cant_create_team(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.post(reverse("account:teams-list"), data=self.data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_cant_update_foreign_team(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.put(reverse("account:teams-detail", kwargs={"pk": self.team.id}), data=self.update_data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_manager_can_get_list_team(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(reverse("account:teams-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.team.title)

    def test_manager_can_get_detail_team(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.team.title)
    
    def test_manager_cant_delete_foreign_team(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.delete(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    



    