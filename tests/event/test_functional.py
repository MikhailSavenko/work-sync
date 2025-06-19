from tests.account.test_functional import ApiTestCaseBase
from django.urls import reverse

from rest_framework import status


class MeetingApiTestCase(ApiTestCaseBase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.meeting_valid_data = {
            "description": "My Meeting",
            "datetime": (cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS).strftime("%Y-%m-%dT%H:%M"),
            "workers": [
              cls.worker_admin.id
            ]
        }

        cls.meeting_no_valid_data = {
            "description": [],
            "datetime": (cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS).strftime("%Y-%m-%dT%H:%M:%S"),
            "workers": [
              "dd"
            ]
        }

    def test_get_list_meeting(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("event:meeting-list"))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                meeting_data = response.data[0]
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

    def test_get_detail_meeting(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("event:meeting-detail", kwargs={"pk": self.meeting.id}))

                self.assertEqual(response.status_code, status.HTTP_200_OK)

                meeting_data = response.data
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
    
    def test_get_detail__not_found_meeting(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("event:meeting-detail", kwargs={"pk": self.ONE_HUNDRED}))

                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_me_param_done_wrong_meeting(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("event:meeting-me"), data={"done": self.SOME_STR})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_me_no_param_wrong_meeting(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("event:meeting-me"))
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                if user in (self.user_normal, self.user_manager):
                    meeting_data = response.data[0]
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

    def test_normal_create_input_valid_data_meeting(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.post(reverse("event:meeting-list"), data=self.meeting_valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        meeting_data = response.data
        self.assertIn("id", meeting_data)
        self.assertIn("description", meeting_data)
        self.assertIn("datetime", meeting_data)
        self.assertIn("creator", meeting_data)
        worker_meeting = meeting_data["workers"]
        self.assertEqual(type(worker_meeting), list)
    
    def test_manager_create_input_valid_data_meeting(self):
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.post(reverse("event:meeting-list"), data=self.meeting_valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        meeting_data = response.data
        self.assertIn("id", meeting_data)
        self.assertIn("description", meeting_data)
        self.assertIn("datetime", meeting_data)
        self.assertIn("creator", meeting_data)
        worker_meeting = meeting_data["workers"]
        self.assertEqual(type(worker_meeting), list)
    
    def test_admin_create_input_valid_data_meeting(self):
        self.client.force_authenticate(user=self.user_admin1)
        response = self.client.post(reverse("event:meeting-list"), data=self.meeting_valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        meeting_data = response.data
        self.assertIn("id", meeting_data)
        self.assertIn("description", meeting_data)
        self.assertIn("datetime", meeting_data)
        self.assertIn("creator", meeting_data)
        worker_meeting = meeting_data["workers"]
        self.assertEqual(type(worker_meeting), list)
    
    def test_create_input_no_valid_data_meeting(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
       
                response = self.client.post(reverse("event:meeting-list"), data=self.meeting_no_valid_data, format="json")

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertCountEqual(["description", "datetime", "workers"], response.json())
              
    def test_update_input_valid_data_meeting(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.put(reverse("event:meeting-detail", kwargs={"pk": self.meeting.id}), data=self.meeting_valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        meeting_data = response.data
        self.assertIn("id", meeting_data)
        self.assertEqual(meeting_data["id"], self.meeting.id)
        
        self.assertIn("description", meeting_data)
        self.assertEqual(meeting_data["description"], self.meeting_valid_data["description"])
        
        self.assertIn("datetime", meeting_data)
        
        self.assertIn("creator", meeting_data)
        self.assertEqual(meeting_data["creator"], self.meeting.creator.id)
        
        worker_meeting = meeting_data["workers"]
        self.assertEqual(type(worker_meeting), list)

    def test_update_no_owner_meeting(self):
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.put(reverse("event:meeting-detail", kwargs={"pk": self.meeting.id}), data=self.meeting_valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_no_valid_data_meeting(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.put(reverse("event:meeting-detail", kwargs={"pk": self.meeting.id}), data=self.meeting_no_valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertCountEqual(["description", "datetime", "workers"], response.json())
