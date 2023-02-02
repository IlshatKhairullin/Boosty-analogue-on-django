from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework import status

from api.serializers import PostSerializer
from web.models import Post


@api_view()
def status_view(request):
    return Response({"status": "ok"})


@api_view(["GET", "POST"])
def posts_view(request):
    if request.method == "POST":
        serializer = PostSerializer(
            data=request.data, context={"request": request}
        )  # переводим данные которые пришли в питоновкий тип
        serializer.is_valid(raise_exception=True)  # если будут ошибки, то они будут сразу выводится на экран
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)  # many = True, тк постов много
    return Response(serializer.data)


@api_view(["GET", "PUT"])
def post_view(request, id: int):
    post = get_object_or_404(Post, id=id)

    # Put - обновление части данных у объекта
    if request.method == "PUT":
        serializer = PostSerializer(instance=post, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )  # либо 200 возвращаем, если фронтенд попросит вернуть обновленные данные

    serializer = PostSerializer(post)  # возвращаем объекты - передаем данные позиционным аргументом
    return Response(serializer.data)
