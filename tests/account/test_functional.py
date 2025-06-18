from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from tests.factories import UserFactory, TeamFactory
from account.models import Worker, Team

from django.urls import reverse


class ApiTestCaseBase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Создадим admin_team Worker
        cls.user_admin = UserFactory()
        cls.worker_admin = cls.user_admin.worker
        cls.worker_admin.role = Worker.Role.ADMIN_TEAM
        cls.worker_admin.save()

        # Создадим normal Worker
        cls.user_normal = UserFactory()
        cls.worker_normal = cls.user_normal.worker

        # Создадим admin_team Worker 2
        cls.user_admin1 = UserFactory()
        cls.worker_admin1 = cls.user_admin1.worker
        cls.worker_admin1.role = Worker.Role.ADMIN_TEAM
        cls.worker_admin1.save()

        # Создадим manager Worker
        cls.user_manager = UserFactory()
        cls.worker_manager = cls.user_manager.worker
        cls.worker_manager.role = Worker.Role.MANAGER
        cls.worker_manager.save()


class TeamApiTestCase(ApiTestCaseBase):

    ONE = 1

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        
        cls.data_team = {
            "title": "Test Team",
            "description": "Test descript =)",
            "workers": [
              cls.worker_admin.id
            ]
        }
        cls.update_data_team = {
            "title": "Test Team Update",
            "description": "Test descript Update =)",
            "workers": [
              cls.worker_admin.id
            ]
        }

        cls.team = TeamFactory(creator=cls.worker_admin)
        cls.team2 = TeamFactory(creator=cls.worker_admin)
        cls.worker_normal.team = cls.team2
        cls.worker_normal.save()

        cls.data_team_conflict = {
            "title": "Test Team Conflict",
            "description": "Test descript Conflict=)",
            "workers": [
              cls.worker_normal.id
            ]
        }
    
    def test_check_team_conflict_create_team_pk_none(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.post(reverse("account:teams-list"), data=self.data_team_conflict, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    
    def test_check_team_conflict_update_team_pk_not_none(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.put(reverse("account:teams-detail", kwargs={"pk": self.team.id}), data=self.data_team_conflict, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_admin_can_create_team(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.post(reverse("account:teams-list"), data=self.data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.data_team["title"])
        self.assertEqual(response.data["description"], self.data_team["description"])
    
    def test_admin_can_update_his_team(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.put(reverse("account:teams-detail", kwargs={"pk": self.team.id}), data=self.update_data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.update_data_team["title"])
        self.assertEqual(response.data["description"], self.update_data_team["description"])
    
    def test_admin_can_get_list_team(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(reverse("account:teams-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.team.title)

    def test_admin_can_get_detail_team(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.get(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.team.title)
    
    def test_admin_can_delete_his_team(self):
        team_count = Team.objects.count()
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.delete(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(team_count - self.ONE, Team.objects.count())
    
    def test_admin_cant_delete_foreign_team(self):
        self.client.force_authenticate(user=self.user_admin1)
        response = self.client.delete(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_cant_create_team(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.post(reverse("account:teams-list"), data=self.data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_cant_update_foreign_team(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.put(reverse("account:teams-detail", kwargs={"pk": self.team.id}), data=self.update_data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_normal_can_get_list_team(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.get(reverse("account:teams-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.team.title)

    def test_normal_can_get_detail_team(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.get(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.team.title)
    
    def test_normal_cant_delete_foreign_team(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.delete(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_manager_cant_create_team(self):
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.post(reverse("account:teams-list"), data=self.data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_cant_update_foreign_team(self):
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.put(reverse("account:teams-detail", kwargs={"pk": self.team.id}), data=self.update_data_team, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_manager_can_get_list_team(self):
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.get(reverse("account:teams-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.team.title)

    def test_manager_can_get_detail_team(self):
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.get(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.team.title)
    
    def test_manager_cant_delete_foreign_team(self):
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.delete(reverse("account:teams-detail", kwargs={"pk": self.team.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

class WorkerApiTestCase(ApiTestCaseBase):
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_normal_get_list_worker(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.get(reverse("account:worker-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

        worker_data = response.data[0]

        # Проверяем наличие ключевых полей на верхнем уровне
        self.assertIn("id", worker_data)
        self.assertIn("team", worker_data)
        self.assertIn("role", worker_data)
        self.assertIn("user_id", worker_data)
        self.assertIn("first_name", worker_data)
        self.assertIn("last_name", worker_data)
        self.assertIn("email", worker_data)

        if worker_data["team"] is not None:
            team_data = worker_data["team"]
            self.assertIn("id", team_data)
            self.assertIn("title", team_data)
            self.assertIsInstance(team_data["id"], int)
            self.assertIsInstance(team_data["title"], str)




