from tests.account.test_functional import ApiTestCaseBase
from django.urls import reverse

from rest_framework import status


class MeetingApiTestCase(ApiTestCaseBase):

    @classmethod
    def setUpTestData(self):
        super().setUpTestData()

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
