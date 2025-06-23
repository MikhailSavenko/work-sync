import datetime
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from task.models import Task
from tests.factories import EvaluationFactory, UserFactory, TeamFactory, TaskFactory, MeetingFactory
from account.models import Worker, Team

from django.urls import reverse


class ApiTestCaseBase(APITestCase):
    ONE = 1
    ZERO = 0

    ONE_HUNDRED = 100

    FIVE_FLOAT = 5.0

    SOME_STR = "some string"

    SOME_STR_ANOTHER = "some string another"

    SOME_STR_MORE = "more string"

    DATETIME_NOW = datetime.datetime.now(datetime.timezone.utc)
    TIMEDELTA_THREE_DAYS = datetime.timedelta(days=3)
    
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
        
        # Создадим normal Worker 1
        cls.user_normal1 = UserFactory()
        cls.worker_normal1 = cls.user_normal1.worker

        # Создадим normal Worker 2
        cls.user_normal2 = UserFactory()
        cls.worker_normal2 = cls.user_normal2.worker

        # Создадим normal Worker 3
        cls.user_normal3 = UserFactory()
        cls.worker_normal3 = cls.user_normal3.worker

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

        # Создадим manager Worker
        cls.user_manager1 = UserFactory()
        cls.worker_manager1 = cls.user_manager1.worker
        cls.worker_manager1.role = Worker.Role.MANAGER
        cls.worker_manager1.save()

        cls.user_role_all = (cls.user_normal, cls.user_manager, cls.user_admin)

        cls.meeting = MeetingFactory(datetime=(cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS), creator=cls.worker_normal)
        cls.meeting.workers.set([cls.worker_normal, cls.worker_manager])
        
        datetime_with_second = (cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS)
        no_second_datetime = datetime_with_second.replace(second=0, microsecond=0)
        cls.meeting1 = MeetingFactory(datetime=no_second_datetime, creator=cls.worker_normal1)
        cls.meeting1.workers.set([cls.worker_normal1])

        cls.meeting2 = MeetingFactory(datetime=no_second_datetime, creator=cls.worker_normal1)
        cls.meeting2.workers.set([cls.worker_normal2])


class TeamApiTestCase(ApiTestCaseBase):

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
        cls.task_done = TaskFactory(creator=cls.worker_manager, executor=cls.worker_normal, status=Task.StatusTask.DONE, deadline=(cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS))
        
        cls.evaluation = EvaluationFactory(to_worker=cls.worker_normal, task=cls.task_done)

        cls.team = TeamFactory(creator=cls.worker_admin)
        cls.worker_normal.team = cls.team
        cls.worker_normal.save()

        cls.role_no_valid_data = {
            "role": "MN"
        }
        cls.role_manager_data = {
            "role": "MG"
        }

    def test_get_list_worker(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("account:worker-list"))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertIsInstance(response.data, list)
                self.assertGreater(len(response.data), 0)

                worker_data = response.data[1]

                self.assertIn("id", worker_data)
                self.assertIn("team", worker_data)
                self.assertIn("role", worker_data)
                self.assertIn("user_id", worker_data)
                self.assertIn("first_name", worker_data)
                self.assertIn("last_name", worker_data)
                self.assertIn("email", worker_data)

                team_data = worker_data["team"]
                self.assertIn("id", team_data)
                self.assertIn("title", team_data)
                self.assertIsInstance(team_data["id"], int)
                self.assertIsInstance(team_data["title"], str)

    def test_get_detail_worker(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("account:worker-detail", kwargs={"pk": self.worker_normal.id}))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertIsInstance(response.data, dict)

                worker_data = response.data

                self.assertIn("id", worker_data)
                self.assertIn("team", worker_data)
                self.assertIn("role", worker_data)
                self.assertIn("user_id", worker_data)
                self.assertIn("first_name", worker_data)
                self.assertIn("last_name", worker_data)
                self.assertIn("email", worker_data)

                team_data = worker_data["team"]
                self.assertIn("id", team_data)
                self.assertIn("title", team_data)
                self.assertIsInstance(team_data["id"], int)
                self.assertIsInstance(team_data["title"], str)

    def test_get_evaluation_avg_none_score_worker(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                start_date = (self.DATETIME_NOW - self.TIMEDELTA_THREE_DAYS).date().strftime("%Y-%m-%d")
                end_date = (self.DATETIME_NOW - self.TIMEDELTA_THREE_DAYS).date().strftime("%Y-%m-%d")
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("account:worker-average-evaluation", kwargs={"pk": self.worker_normal.id,
                                                                                                "start_date": start_date, 
                                                                                                "end_date": end_date}))
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                data = response.data

                self.assertIn("start_date", data)
                self.assertIn("end_date", data)
                self.assertIn("average_score", data)
                self.assertIn("evaluations_count", data)

                self.assertEqual(data["start_date"], start_date)
                self.assertEqual(data["end_date"], end_date)
                self.assertEqual(data["average_score"], None)
                self.assertEqual(data["evaluations_count"], self.ZERO)
        
    def test_get_evaluation_avg_score_worker(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                start_date = (self.DATETIME_NOW - self.TIMEDELTA_THREE_DAYS).strftime("%Y-%m-%d")
                end_date = (self.DATETIME_NOW + self.TIMEDELTA_THREE_DAYS).strftime("%Y-%m-%d")
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("account:worker-average-evaluation", kwargs={"pk": self.worker_normal.id,
                                                                                                "start_date": start_date, 
                                                                                                "end_date": end_date}))
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                data = response.data

                self.assertIn("start_date", data)
                self.assertIn("end_date", data)
                self.assertIn("average_score", data)
                self.assertIn("evaluations_count", data)

                self.assertEqual(data["start_date"], start_date)
                self.assertEqual(data["end_date"], end_date)
                self.assertEqual(data["average_score"], self.FIVE_FLOAT)
                self.assertEqual(data["evaluations_count"], self.ONE)
        
    def test_get_calendar_day_worker(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                date = (self.DATETIME_NOW + self.TIMEDELTA_THREE_DAYS).date().strftime("%Y-%m-%d")
                response = self.client.get(reverse("account:worker-calendar-day", kwargs={"pk": self.worker_normal.id,
                                                                                          "date": date}))
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                data = response.data

                self.assertIn("date", data)
                self.assertIn("meetings", data)
                self.assertIn("tasks", data)
                self.assertIn("table", data)

                self.assertEqual(type(data["table"]), list)

                tasks_data = data["tasks"][0]
                self.assertEqual(len(data["tasks"]), self.ONE)
                self.assertIn("id", tasks_data)
                self.assertIn("title", tasks_data)
                self.assertIn("description", tasks_data)
                self.assertIn("deadline", tasks_data)
                self.assertIn("status", tasks_data)

                self.assertIn("executor", tasks_data)

                executor_task = tasks_data["executor"]
                self.assertIn("id", executor_task)
                self.assertIn("full_name", executor_task)
                self.assertIn("role", executor_task)
                self.assertIn("team", executor_task)

                self.assertIn("creator", tasks_data)

                creator_task = tasks_data["creator"]
                self.assertIn("id", creator_task)
                self.assertIn("full_name", creator_task)
                self.assertIn("role", creator_task)
                self.assertIn("team", creator_task)

                self.assertIn("evaluation", tasks_data)
                self.assertIn("created_at", tasks_data)
                self.assertIn("updated_at", tasks_data)

                meeting_data = data["meetings"][0]
                self.assertEqual(len(data["meetings"]), self.ONE)
                self.assertIn("id", meeting_data)
                self.assertIn("description", meeting_data)
                self.assertIn("datetime", meeting_data)
                self.assertIn("creator", meeting_data)
                self.assertEqual(meeting_data["creator"], self.worker_normal.id)

                self.assertIn("workers", meeting_data)

                worker_meeting = meeting_data["workers"][0]
                self.assertEqual(type(meeting_data["workers"]), list)
                self.assertIn("id", worker_meeting)
                self.assertIn("full_name", worker_meeting)
                self.assertIn("role", worker_meeting)
                self.assertIn("team", worker_meeting)
    
    def test_get_calendar_day_not_found_worker(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=self.user_normal)
                date = (self.DATETIME_NOW + self.TIMEDELTA_THREE_DAYS).date().strftime("%Y-%m-%d")
                response = self.client.get(reverse("account:worker-calendar-day", kwargs={"pk": self.ONE_HUNDRED,
                                                                                          "date": date}))

                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_calendar_month_worker(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                date = (self.DATETIME_NOW + self.TIMEDELTA_THREE_DAYS).date().strftime("%Y-%m")
                response = self.client.get(reverse("account:worker-calendar-month", kwargs={"pk": self.worker_normal.id,
                                                                                          "date": date}))

                self.assertEqual(response.status_code, status.HTTP_200_OK)

                data = response.data

                self.assertIn("date", data)
                self.assertIn("meetings", data)
                self.assertIn("tasks", data)
                self.assertIn("table", data)

                self.assertEqual(type(data["table"]), list)

                tasks_data = data["tasks"][0]
                self.assertEqual(len(data["tasks"]), self.ONE)
                self.assertIn("id", tasks_data)
                self.assertIn("title", tasks_data)
                self.assertIn("description", tasks_data)
                self.assertIn("deadline", tasks_data)
                self.assertIn("status", tasks_data)

                self.assertIn("executor", tasks_data)

                executor_task = tasks_data["executor"]
                self.assertIn("id", executor_task)
                self.assertIn("full_name", executor_task)
                self.assertIn("role", executor_task)
                self.assertIn("team", executor_task)

                self.assertIn("creator", tasks_data)

                creator_task = tasks_data["creator"]
                self.assertIn("id", creator_task)
                self.assertIn("full_name", creator_task)
                self.assertIn("role", creator_task)
                self.assertIn("team", creator_task)

                self.assertIn("evaluation", tasks_data)
                self.assertIn("created_at", tasks_data)
                self.assertIn("updated_at", tasks_data)

                meeting_data = data["meetings"][0]
                self.assertEqual(len(data["meetings"]), self.ONE)
                self.assertIn("id", meeting_data)
                self.assertIn("description", meeting_data)
                self.assertIn("datetime", meeting_data)
                self.assertIn("creator", meeting_data)
                self.assertEqual(meeting_data["creator"], self.worker_normal.id)

                self.assertIn("workers", meeting_data)

                worker_meeting = meeting_data["workers"][0]
                self.assertEqual(type(meeting_data["workers"]), list)
                self.assertIn("id", worker_meeting)
                self.assertIn("full_name", worker_meeting)
                self.assertIn("role", worker_meeting)
                self.assertIn("team", worker_meeting)

    def test_normal_partial_update_worker(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.patch(reverse("account:worker-detail", kwargs={"pk": self.worker_normal.id}), data=self.role_manager_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user_manager)
        date = (self.DATETIME_NOW + self.TIMEDELTA_THREE_DAYS).date().strftime("%Y-%m")
        response = self.client.get(reverse("account:worker-calendar-month", kwargs={"pk": self.worker_normal.id,
                                                                                  "date": date}))
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        
        self.assertIn("date", data)
        self.assertIn("meetings", data)
        self.assertIn("tasks", data)
        self.assertIn("table", data)

        self.assertEqual(type(data["table"]), list)

        tasks_data = data["tasks"][0]
        self.assertEqual(len(data["tasks"]), self.ONE)
        self.assertIn("id", tasks_data)
        self.assertIn("title", tasks_data)
        self.assertIn("description", tasks_data)
        self.assertIn("deadline", tasks_data)
        self.assertIn("status", tasks_data)
       
        self.assertIn("executor", tasks_data)
        
        executor_task = tasks_data["executor"]
        self.assertIn("id", executor_task)
        self.assertIn("full_name", executor_task)
        self.assertIn("role", executor_task)
        self.assertIn("team", executor_task)

        self.assertIn("creator", tasks_data)
        
        creator_task = tasks_data["creator"]
        self.assertIn("id", creator_task)
        self.assertIn("full_name", creator_task)
        self.assertIn("role", creator_task)
        self.assertIn("team", creator_task)

        self.assertIn("evaluation", tasks_data)
        self.assertIn("created_at", tasks_data)
        self.assertIn("updated_at", tasks_data)

        meeting_data = data["meetings"][0]
        self.assertEqual(len(data["meetings"]), self.ONE)
        self.assertIn("id", meeting_data)
        self.assertIn("description", meeting_data)
        self.assertIn("datetime", meeting_data)
        self.assertIn("creator", meeting_data)
        self.assertEqual(meeting_data["creator"], self.worker_normal.id)

        self.assertIn("workers", meeting_data)

        worker_meeting = meeting_data["workers"][0]
        self.assertEqual(type(meeting_data["workers"]), list)
        self.assertIn("id", worker_meeting)
        self.assertIn("full_name", worker_meeting)
        self.assertIn("role", worker_meeting)
        self.assertIn("team", worker_meeting)

    def test_manager_partial_update_worker(self):
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.patch(reverse("account:worker-detail", kwargs={"pk": self.worker_normal.id}), data=self.role_manager_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_partial_update_no_valid_worker(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.patch(reverse("account:worker-detail", kwargs={"pk": self.worker_normal.id}), data=self.role_no_valid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_admin_partial_update_valid_data_worker(self):
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.patch(reverse("account:worker-detail", kwargs={"pk": self.worker_normal.id}), data=self.role_manager_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("role", response.data)
        self.assertEqual(response.data["role"], self.role_manager_data["role"])
    

