from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from task.views import CommentViewSet, EvaluationViewSet, TaskViewSet

app_name = "task"


router = SimpleRouter()

router.register(r"tasks", TaskViewSet, basename="tasks")

nested_router = NestedSimpleRouter(router, r"tasks", lookup="task")
nested_router.register(r"comments", CommentViewSet, basename="comment")
nested_router.register(r"evaluations", EvaluationViewSet, basename="evaluation")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(nested_router.urls)),
]
