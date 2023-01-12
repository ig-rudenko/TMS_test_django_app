from django.urls import path, re_path
from test_app import views

# /posts/
urlpatterns = [
    path("create/", views.CreatePost.as_view(), name="create-post"),
    re_path("^(?P<post_id>[0-9]+)/$", views.ShowPost.as_view(), name="show-post"),
    path("<int:post_id>/update/", views.UpdatePost.as_view(), name="update-post"),
    path("<int:post_id>/delete/", views.DeletePost.as_view(), name="delete-post"),
]
