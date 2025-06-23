from django.urls import reverse
from task.models import Comment, Task
from tests.account.test_functional import ApiTestCaseBase
from tests.factories import CommentFactory, TaskFactory
from rest_framework import status


class TaskApiTestCase(ApiTestCaseBase):
    DEADLINE_NOT_IN_THE_PAST_STR = "Дэдлайн не может быть в прошлом."

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData() 

        cls.task = TaskFactory(creator=cls.worker_manager, executor=cls.worker_normal, deadline=(cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS))
        cls.task1 = TaskFactory(creator=cls.worker_admin, executor=cls.worker_normal, deadline=(cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS))

        cls.valid_data_task = {
            "title": "New Test Task",
            "description": "Task description",
            "deadline": (cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS).strftime("%Y-%m-%dT%H:%M"),
            "executor": cls.worker_normal2.id
        }
        cls.no_valid_data_task = {
            "title": ["New Test Task"],
            "description": ["Task description"],
            "deadline": "2020-20-20",
            "executor": "ss"
        }
        cls.deadline_in_the_past_data = {
            "title": "in the past",
            "description": "Task description",
            "deadline": (cls.DATETIME_NOW - cls.TIMEDELTA_THREE_DAYS).strftime("%Y-%m-%dT%H:%M"),
            "executor": cls.worker_normal2.id
        }
        cls.valid_update_data_task = {
            "title": "valid update",
            "description": "update description",
            "status": "DN",
            "deadline": (cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS + cls.TIMEDELTA_THREE_DAYS).strftime("%Y-%m-%dT%H:%M"),
            "executor": cls.worker_normal2.id
        }
        cls.no_valid_update_data_task = {
            "title": ["New Test Task"],
            "description": ["Task description"],
            "deadline": "2020-20-20",
            "status": "sss",
            "executor": "ss"
        }
        cls.valid_partial_upd_status_data = {
            "status": "DN"
        }

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
    
    def _assert_task_response_create_structure(self, task_data):
        self.assertIn("id", task_data)
        self.assertIn("title", task_data)
        self.assertIn("description", task_data)
        self.assertIn("deadline", task_data)
        self.assertIn("status", task_data)
        self.assertIn("executor", task_data)
        self.assertIn("creator", task_data)

    def _assert_task_check_value_with_task(self, task_data):
        self.assertEqual(task_data["id"], self.task.id)
        self.assertEqual(task_data["title"], self.task.title)
        self.assertEqual(task_data["description"], self.task.description)
        self.assertEqual(task_data["status"], Task.StatusTask.OPEN.label)
        self.assertEqual(task_data["executor"]["id"], self.task.executor.id)
        self.assertEqual(task_data["creator"]["id"], self.task.creator.id)

    def _assert_task_check_input_data_with_db(self, task_data, db_qs, worker):
        self.assertEqual(db_qs.title, task_data["title"])
        self.assertEqual(db_qs.description, task_data["description"])
        self.assertEqual(db_qs.executor.id, task_data["executor"])
        self.assertEqual(db_qs.creator.id, worker.id)

    def test_get_list_task(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:tasks-list"))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                data = response.json()
                task_data = data[0]
                self.assertIsInstance(data, list)
                self._assert_task_detail_structure(task_data)
                self._assert_task_check_value_with_task(task_data=task_data)

    def test_get_detail_task(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:tasks-detail", kwargs={"pk": self.task.id}))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                data = response.json()
                task_data = data
                self.assertIsInstance(task_data, dict)
                self._assert_task_detail_structure(task_data)
                self._assert_task_check_value_with_task(task_data=task_data)
    
    def test_get_me_task(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:tasks-me"))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                if user == self.user_normal:
                    data = response.json()
                    task_data = data[0]
                    self.assertIsInstance(data, list)
                    self._assert_task_detail_structure(task_data)     
                    self._assert_task_check_value_with_task(task_data=task_data)    
    
    def test_normal_create_input_valid_data_task(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.post(reverse("task:tasks-list"), data=self.valid_data_task, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_manager_create_input_valid_data_task(self):
        count_tasks = Task.objects.count()
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.post(reverse("task:tasks-list"), data=self.valid_data_task, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_data = response.json()
        self._assert_task_response_create_structure(task_data=task_data)
        self.assertEqual(count_tasks + self.ONE, Task.objects.count())

        created_task_id = task_data["id"]
        try:
            task_in_db = Task.objects.get(id=created_task_id)
            self._assert_task_check_input_data_with_db(db_qs=task_in_db, task_data=task_data, worker=self.worker_manager)
        except Task.DoesNotExist:
            self.fail(f"Task with ID {created_task_id} was not found in the database after manager creation. Response: {response.json()}")
    
    def test_admin_create_input_valid_data_task(self):
        count_tasks = Task.objects.count()
        self.client.force_authenticate(user=self.user_admin)
        response = self.client.post(reverse("task:tasks-list"), data=self.valid_data_task, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_data = response.json()
        self._assert_task_response_create_structure(task_data=task_data)
        self.assertEqual(count_tasks + self.ONE, Task.objects.count())

        created_task_id = task_data["id"]
        try:
            task_in_db = Task.objects.get(id=created_task_id)
            self._assert_task_check_input_data_with_db(db_qs=task_in_db, task_data=task_data, worker=self.worker_admin)
        except Task.DoesNotExist:
            self.fail(f"Task with ID {created_task_id} was not found in the database after admin creation. Response: {response.json()}")

    def test_create_no_valid_data_task(self):
        for user in [self.user_admin, self.user_manager]:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.post(reverse("task:tasks-list"), data=self.no_valid_data_task, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertCountEqual(["description", "deadline", "title", "executor"], response.json())
    
    def test_create_deadline_in_the_past_data_task(self):
        for user in [self.user_admin, self.user_manager]:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.post(reverse("task:tasks-list"), data=self.deadline_in_the_past_data, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertCountEqual(["deadline"], response.json())
                self.assertEqual(response.json()["deadline"][0], self.DEADLINE_NOT_IN_THE_PAST_STR)
    
    def test_update_manager_or_admin_owner_input_valid_data_task(self):
        params_user_task = {
            self.user_manager: self.task.id,
            self.user_admin: self.task1.id
        }
        for user, task in params_user_task.items():
            with self.subTest(user=user, task=task):
                self.client.force_authenticate(user=user)
                response = self.client.put(reverse("task:tasks-detail", kwargs={"pk": task}), data=self.valid_update_data_task, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                task_data = response.json()
                created_task_id = task_data["id"]
                try:
                    task_in_db = Task.objects.get(id=created_task_id)
                    self._assert_task_check_input_data_with_db(db_qs=task_in_db, task_data=task_data, worker=user.worker)
                    self.assertEqual(task_data["status"], task_in_db.status)
                except Task.DoesNotExist:
                    self.fail(f"Task with ID {created_task_id} was not found in the database after manager creation. Response: {response.json()}")

    def test_update_manager_or_admin_not_owner_input_valid_data_task(self):
        params_user_task = {
            self.user_manager1: self.task.id,
            self.user_admin1: self.task1.id
        }
        for user, task in params_user_task.items():
            with self.subTest(user=user, task=task):
                self.client.force_authenticate(user=user)
                response = self.client.put(reverse("task:tasks-detail", kwargs={"pk": task}), data=self.valid_update_data_task, format="json")
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                
    def test_update_normal_no_owner_task(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.put(reverse("task:tasks-detail", kwargs={"pk": self.task.id}), data=self.valid_update_data_task, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_upd_normal_no_owner_task(self):
        self.client.force_authenticate(user=self.user_normal)
        response = self.client.patch(reverse("task:tasks-detail", kwargs={"pk": self.task.id}), data=self.valid_partial_upd_status_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_partial_upd_manager_or_admin_owner_input_valid_field_status_data_task(self):
        params_user_task = {
            self.user_manager: self.task.id,
            self.user_admin: self.task1.id
        }
        for user, task in params_user_task.items():
            with self.subTest(user=user, task=task):
                self.client.force_authenticate(user=user)

                try:
                    task_in_db = Task.objects.get(id=task)
                    status_befor_partial_upd = task_in_db.status
                    self.assertEqual(status_befor_partial_upd, Task.StatusTask.OPEN)
                except Task.DoesNotExist:
                    self.fail(f"Task with ID {task.id} was not found in the database.")

                response = self.client.patch(reverse("task:tasks-detail", kwargs={"pk": task}), data=self.valid_partial_upd_status_data, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                task_data = response.json()
                created_task_id = task_data["id"]
                try:
                    task_in_db = Task.objects.get(id=created_task_id)
                    self._assert_task_check_input_data_with_db(db_qs=task_in_db, task_data=task_data, worker=user.worker)
                    self.assertEqual(task_data["status"], task_in_db.status)
                except Task.DoesNotExist:
                    self.fail(f"Task with ID {created_task_id} was not found in the database after {user.worker.role} partial updated. Response: {response.json()}")

    def test_partial_upd_manager_or_admin_owner_input_valid_data_task(self):
        params_user_task = {
            self.user_manager: self.task.id,
            self.user_admin: self.task1.id
        }
        for user, task in params_user_task.items():
            with self.subTest(user=user, task=task):
                self.client.force_authenticate(user=user)
                response = self.client.patch(reverse("task:tasks-detail", kwargs={"pk": task}), data=self.valid_update_data_task, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                task_data = response.json()
                created_task_id = task_data["id"]
                try:
                    task_in_db = Task.objects.get(id=created_task_id)
                    self._assert_task_check_input_data_with_db(db_qs=task_in_db, task_data=task_data, worker=user.worker)
                    self.assertEqual(task_data["status"], task_in_db.status)
                except Task.DoesNotExist:
                    self.fail(f"Task with ID {created_task_id} was not found in the database after {user.worker.role} partial update. Response: {response.json()}")

    def test_update_no_valid_data_task(self):
        params_user_task = {
            self.user_manager: self.task.id,
            self.user_admin: self.task1.id
        }
        for user, task in params_user_task.items():
            with self.subTest(user=user, task=task):
                self.client.force_authenticate(user=user)
                response = self.client.put(reverse("task:tasks-detail", kwargs={"pk": task}), data=self.no_valid_update_data_task, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertCountEqual(["description", "deadline", "title", "executor", "status"], response.json())
    
    def test_partial_upd_no_valid_data_task(self):
        params_user_task = {
            self.user_manager: self.task.id,
            self.user_admin: self.task1.id
        }
        for user, task in params_user_task.items():
            with self.subTest(user=user, task=task):
                self.client.force_authenticate(user=user)
                response = self.client.patch(reverse("task:tasks-detail", kwargs={"pk": task}), data=self.no_valid_update_data_task, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertCountEqual(["description", "deadline", "title", "executor", "status"], response.json())
    

class CommentApiTestCase(ApiTestCaseBase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.task = TaskFactory(creator=cls.worker_manager, executor=cls.worker_normal, deadline=(cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS))
        cls.comment = CommentFactory(task=cls.task, creator=cls.worker_normal, text=cls.SOME_STR)
        cls.comment1 = CommentFactory(task=cls.task, creator=cls.worker_manager, text=cls.SOME_STR_ANOTHER)

    def _assert_fields_in_json_comment(self, comment_data: dict):
        self.assertIn("id", comment_data)
        self.assertIn("task", comment_data)
        self.assertIn("text", comment_data)
        self.assertIn("creator", comment_data)
        self.assertIn("created_at", comment_data)
        self.assertIn("updated_at", comment_data)

    def _assert_compare_value_with_db_comment(self, db_obj, comment_data: dict):
        self.assertEqual(comment_data["id"], db_obj.id)
        self.assertEqual(comment_data["task"], db_obj.task.id)
        self.assertEqual(comment_data["text"], db_obj.text)
        self.assertEqual(comment_data["creator"], db_obj.creator.id)

    def test_get_list_comment(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:comment-list", kwargs={"task_pk": self.task.id}))
                
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                comment_data = response.json()[0]   
                self._assert_fields_in_json_comment(comment_data=comment_data)

                try:
                    com_id = comment_data["id"] 
                    comment_db = Comment.objects.get(id=com_id)
                    self._assert_compare_value_with_db_comment(comment_data=comment_data, db_obj=comment_db)
                except Comment.DoesNotExist:
                    self.fail(f"Comment with {comment_db} does not exist in DB! :O")

    def test_get_list_not_found_task_pk_comment(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:comment-list", kwargs={"task_pk": self.ONE_HUNDRED}))
                
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_list_no_valid_task_pk_comment(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:comment-list", kwargs={"task_pk": self.SOME_STR}))
                
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_detail_comment(self):
        for user in self.user_role_all:
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:comment-detail", kwargs={"task_pk": self.task.id, "pk": self.comment.id}))
                
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                comment_data = response.json()  
                self._assert_fields_in_json_comment(comment_data=comment_data)

                try:
                    comment_db = Comment.objects.get(id=self.comment.id)
                    self._assert_compare_value_with_db_comment(comment_data=comment_data, db_obj=comment_db)
                except Comment.DoesNotExist:
                    self.fail(f"Comment with {comment_db} does not exist in DB! :O")

    def test_get_detail_not_found_comment(self):
        input_sub_test_value = (
            (self.user_normal, self.ONE_HUNDRED, self.comment.id),
            (self.user_admin, self.ONE_HUNDRED, self.comment.id),
            (self.user_manager, self.ONE_HUNDRED, self.comment.id),
            (self.user_normal, self.task.id, self.ONE_HUNDRED),
            (self.user_admin, self.task.id, self.ONE_HUNDRED),
            (self.user_manager, self.task.id, self.ONE_HUNDRED),
        )

        for user, task_pk, comment_pk in input_sub_test_value:
            with self.subTest(user=user, task_pk=task_pk, comment_pk=comment_pk):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:comment-detail", kwargs={"task_pk": task_pk, "pk": comment_pk}))
                
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_detail_no_valid_task_pk_comment(self):
        input_sub_test_value = (
            (self.user_normal, self.SOME_STR, self.comment.id),
            (self.user_admin, self.SOME_STR, self.comment.id),
            (self.user_manager, self.SOME_STR, self.comment.id),
        )

        for user, no_valid_task_pk, comment_pk in input_sub_test_value:
            with self.subTest(user=user, task_pk=no_valid_task_pk, comment_pk=comment_pk):
                self.client.force_authenticate(user=user)
                response = self.client.get(reverse("task:comment-detail", kwargs={"task_pk": no_valid_task_pk, "pk": comment_pk}))
                
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_valid_data_comment(self):
        pass