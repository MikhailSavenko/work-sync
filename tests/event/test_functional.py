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
                print(response.data)
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
