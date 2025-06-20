from django.urls import reverse
from tests.account.test_functional import ApiTestCaseBase
from tests.factories import TaskFactory
from rest_framework import status


class TaskApiTestCase(ApiTestCaseBase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData() 

        cls.task = TaskFactory(creator=cls.worker_manager, executor=cls.worker_normal, deadline=(cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS))
    
    def _assert_task_detail_structure(self, task_data):
        """Проверяет общую структуру JSON-представления задачи."""
        self.assertIn("id", task_data)
        self.assertIn("title", task_data)
        self.assertIn("description", task_data)
        self.assertIn("deadline", task_data)
        self.assertIn("status", task_data)
        self.assertIn("executor", task_data)

        executor_task = task_data["executor"]
        self.assertIn("id", executor_task)
        self.assertIn("full_name", executor_task)
        self.assertIn("role", executor_task)
        self.assertIn("team", executor_task)

        self.assertIn("creator", task_data)
        creator_task = task_data["creator"]
        self.assertIn("id", creator_task)
        self.assertIn("full_name", creator_task)
        self.assertIn("role", creator_task)
        self.assertIn("team", creator_task)

        self.assertIn("evaluation", task_data)
        self.assertIn("created_at", task_data)
        self.assertIn("updated_at", task_data)
    
    def test_get_list_task(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:tasks-list"))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                data = response.json()
                tasks_data = data[0]
                self.assertIsInstance(data, list)
                self._assert_task_detail_structure(tasks_data)

    def test_get_detail_task(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:tasks-detail", kwargs={"pk": self.task.id}))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                data = response.json()
                tasks_data = data
                self.assertIsInstance(tasks_data, dict)
                self._assert_task_detail_structure(tasks_data)
    
    def test_get_me_task(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:tasks-me"))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                if user == self.user_normal:
                    data = response.json()
                    tasks_data = data[0]
                    self.assertIsInstance(data, list)
                    self._assert_task_detail_structure(tasks_data)
                    self.assertEqual(tasks_data["id"], self.task.id)
                    self.assertEqual(tasks_data["title"], self.task.title)
                    self.assertEqual(tasks_data["description"], self.task.description)
                    self.assertEqual(tasks_data["status"], self.task.status)
                    self.assertEqual(tasks_data["executor"], self.task.self.task.status)