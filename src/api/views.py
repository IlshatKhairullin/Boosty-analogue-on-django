from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import generics, viewsets
from rest_framework import status

from api.serializers import PostSerializer, UserSerializer, NoteSerializer, StatusSerializer, NoteEditorSerializer
from web.models import Post, User, Note


@swagger_auto_schema(
    method="GET", operation_id="api_status", responses={status.HTTP_200_OK: StatusSerializer()}
)  # operation_id название в redoc
@api_view()
def status_view(request):
    """Status view"""  # название апи метода в swagger
    return Response(StatusSerializer({"status": "ok", "user_id": request.user.id}).data)


@swagger_auto_schema(
    methods=["GET"],
    operation_id="api_posts_get",
    responses={
        status.HTTP_200_OK: PostSerializer(),
    },
)
@swagger_auto_schema(
    methods=["POST"], operation_id="api_posts_post", responses={status.HTTP_201_CREATED: PostSerializer()}
)
@api_view(["GET", "POST"])
def posts_view(request):
    """Post's api"""
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
def post_view(request, pk: int):
    """Single post api"""
    post = generics.get_object_or_404(Post, pk=pk)

    # Put - обновление части данных у объекта
    if request.method == "PUT":
        print(request.data)
        serializer = PostSerializer(instance=post, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )  # либо 200 возвращаем, если фронтенд попросит вернуть обновленные данные

    serializer = PostSerializer(post)  # возвращаем объекты - передаем данные позиционным аргументом
    return Response(serializer.data)


# для того чтобы убрать дублирование кода (одинаковые queryset и serializer_class в классах),
# в viewset'ах внутри реализован весь круд(или не весь, или только на чтение и т д)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NoteViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    page_size = 10
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)  # так можно настраивать специфичную авторизацию для каждого класса
    # закомментировать верхнюю строку для работы с jwt авторизацией, раскомментировать - токены с djoser

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return NoteEditorSerializer
        return NoteSerializer

    def get_queryset(self):
        author = self.request.user
        return Note.objects.select_related("author").filter(author=author)

    @action(methods=["get"], detail=False, description="note_titles")
    def titles(self, request):
        titles = Note.objects.values_list("title", flat=True).exclude(title__exact="")
        # flat - false, значит будут кортежи, exclude - SQL: select ... where NOT (условие), возвращает new queryset
        return Response({"note_titles": [title for title in titles]})

    @action(methods=["get"], detail=True, description="note_title")
    def title(self, request, pk):
        note = get_object_or_404(Note, id=pk)
        return Response({"note_title": note.title})
