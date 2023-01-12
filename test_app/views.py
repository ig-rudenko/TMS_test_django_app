from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Posts
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def has_permission_to_post(func):
    def deco(request, post_id: int, *args, **kwargs):

        post: Posts = get_object_or_404(Posts, id=post_id)

        if request.user.id == post.user.id:
            return func(request, post, *args, **kwargs)
        return HttpResponseForbidden()

    return deco


class ShowAllPosts(View):

    def get(self, request):
        # Все заметки, у которых пользователь содержит в username "test"
        all_posts = Posts.objects.all()

        print(all_posts.query)

        return render(
            request,
            "main.html",
            {"posts": all_posts, "cost": 89787394123.123, "date": datetime.now() - timedelta(hours=49)}
        )


class ShowPost(View):

    def get(self, request, post_id):
        post: Posts = get_object_or_404(Posts, id=post_id)

        print(type(post.user), post.user.__dict__)

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
        print(request.user)
        if title and content:
            self.create(title=title, content=content, user=request.user)
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
        print(kwargs)
        post = self.model(**kwargs)
        post.save()


@method_decorator(login_required, name="dispatch")
@method_decorator(has_permission_to_post, name="dispatch")
class UpdatePost(View):

    def get(self, request, post: Posts):
        return render(
            request,
            "edit.html",
            {
                "title": post.title,
                "content": post.content,
                "post_id": post.id
            }
        )

    def post(self, request, post: Posts):

        print("def post(self, request, post: Posts):")
        print("   ", type(post), post)
        post_id = post.id

        title = request.POST.get("title", "")  # Если нет колюча title, то вернет ""
        content = request.POST.get("content", "")

        if title and content:
            print("# Обновляем конкретные поля в базе")
            # Обновляем конкретные поля в базе

            if Posts.objects.filter(id=post_id).exists():
                print("Заметка найдена")
                print(Posts.objects.filter(id=post_id).update(title=title, content=content))

            return redirect("show-post", post_id)

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
    def post(self, request, post_id: int):
        Posts.objects.filter(id=post_id).delete()
        return redirect("home")
