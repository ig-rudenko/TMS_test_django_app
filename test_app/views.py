from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from .models import Posts
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def show_posts(request):
    """
    Функция представления всех постов
    :param request:
    :return:
    """

    all_posts = Posts.objects.all()
    return render(
        request,
        "main.html",
        {"posts": all_posts}
    )


@login_required
def create_post(request):
    data = {}

    if request.method == "POST":
        title = request.POST.get("title", "")  # Если нет колюча title, то вернет ""
        content = request.POST.get("content", "")
        if title and content:
            post = Posts(title=title, content=content)
            post.save()
            print(post.id, post.title)
            return redirect("home")

        data["title"] = title
        data["content"] = content

    return render(request, "create.html", data)


def get_post(request, post_id: int):
    post: Posts = get_object_or_404(Posts, id=post_id)
    return render(request, "post.html", {"post": post})


@login_required
def update_post(request, post_id: int):
    post: Posts = get_object_or_404(Posts, id=post_id)

    if request.method == "POST":

        title = request.POST.get("title", "")  # Если нет колюча title, то вернет ""
        content = request.POST.get("content", "")

        if title and content:

            post.title = title
            post.content = content

            # Обновляем конкретные поля в базе
            post.save(update_fields=["title", "content"])

            return redirect("show-post", post.id)

    return render(
        request,
        "edit.html",
        {
            "title": post.title,
            "content": post.content,
            "post_id": post_id
        }
    )


@login_required
def delete_post(request, post_id: int):
    if request.method == "POST":
        post: Posts = get_object_or_404(Posts, id=post_id)
        post.delete()
        return redirect("home")

    return HttpResponseNotAllowed(permitted_methods=["POST"])


class ShowAllPosts(View):

    def get(self, request):
        all_posts = Posts.objects.all()
        return render(
            request,
            "main.html",
            {"posts": all_posts, "cost": 89787394123.123, "date": datetime.now() - timedelta(hours=49)}
        )


class ShowPost(View):

    def get(self, request, post_id):
        post: Posts = get_object_or_404(Posts, id=post_id)
        return render(request, "post.html", {"post": post, "number": 55})


@method_decorator(login_required, name="dispatch")
class CreatePost(View):
    template = "create.html"
    model = Posts

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        title = request.POST.get("title", "")  # Если нет колюча title, то вернет ""
        content = request.POST.get("content", "")
        if title and content:
            self.create(title=title, content=content)
            return redirect("home")

        return render(
            request,
            self.template,
            {
                "title": title,
                "content": content
            }
        )

    def create(self, **kwargs):
        post = self.model(**kwargs)
        post.save()


@method_decorator(login_required, name="dispatch")
class UpdatePost(View):

    def get(self, request, post_id):
        post: Posts = get_object_or_404(Posts, id=post_id)
        return render(
            request,
            "edit.html",
            {
                "title": post.title,
                "content": post.content,
                "post_id": post_id
            }
        )

    def post(self, request, post_id):
        post: Posts = get_object_or_404(Posts, id=post_id)

        title = request.POST.get("title", "")  # Если нет колюча title, то вернет ""
        content = request.POST.get("content", "")

        if title and content:
            post.title = title
            post.content = content

            # Обновляем конкретные поля в базе
            post.save(update_fields=["title", "content"])

            return redirect("show-post", post.id)

        return render(
            request,
            "edit.html",
            {
                "title": post.title,
                "content": post.content,
                "post_id": post_id
            }
        )


@method_decorator(login_required, name="dispatch")
class DeletePost(View):

    def post(self, request, post_id):
        post: Posts = get_object_or_404(Posts, id=post_id)
        post.delete()
        return redirect("home")
