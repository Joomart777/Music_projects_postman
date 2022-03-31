"""
Создать проект.

в settings:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'music_db',
        'USER': 'joomart',
        'PASSWORD': '1',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

in Terminal: psql
создать БД: music_db

> migrate

Теперь в БД у нас есть:

                   List of relations
 Schema |            Name            | Type  |  Owner
--------+----------------------------+-------+---------
 public | auth_group                 | table | joomart
 public | auth_group_permissions     | table | joomart
 public | auth_permission            | table | joomart
 public | auth_user                  | table | joomart
 public | auth_user_groups           | table | joomart
 public | auth_user_user_permissions | table | joomart



ДОбавить админа:
./manage.py createsuperuser

Создать приложение:
./manage.py startapp music_app

В _app:
часто работаем в models, views

In models:
Создаем таблицу Category: с полями title
Чтоб таблица заработала новая в БД --> нужноо в Main -- settings:
включить in Apps: 'music_app'
q
--> ./manage.py makemigrations  -- ОБЯЗАТЕЛЬНО, так подготавливает для закидывания в БД, без этой подготовки не вносятся изменения в БД
--> ./manage.py migrate  -- Теперь в БД добавлено наши апп music_app Category
==> music_db=# \dt

music_db=# select * from music_app_category; ==> на автомате создал id (Django)

но чтоб увидеть на сайте, нужно зарегистрировать в админке:
admin.py-->
    from music_app.models import Category (это импортнули Класс Category--> можно автоматом при наведении ошибки Category --> Alt+Enter и выбрать импорт)

    admin.site.register(Category)

Далее добавим в моделс:
 Music -- > какие поля добавить, blank=True (может быть пустым в поле заполнения), null=True(не обязательно, по БД )

добавим переменную COUNTRY для отображения в табл
далее в класс добавить поле country для отображения

Сделать связку один ко многим:
    category = models.ForeignKey(Category, related_name='music', on_delete=models.CASCADE())
 -- related_name для понятия к классу Category, CASCADE -- для связки по удалению, если удалить в головном, удалится инфо и в дочерних

=> ./manage.py makemigrations  --> подготовили 2ую миграцию
=> ./manage.py migrate  -->добавлены миграция проведения, в БД (если посмотреть через \dt)

runserver

--> добавить в admin:
зарегистрировать: admin.site.register(Music)
Импортнуть можно все чтоб кажд раз не импортировать:
from music_app.models import *

--> models:
можно изменить отображения полей в меню, сабкласс:
    class Meta:
        verbose_name_plural = 'Музыка'
        verbose_name = 'Музыка**'

--- Напишем N point, для отображения списка по переходу по адресу сайта (список музыки):
Отображение сайта в views.py:
напишем ф-ю чтоб вытащить инфо из БД:
@api_view(['GET'])
def get_music():
    musics = Music.objects.all()  (если для импорта через Alt+Enter)
    print(musics)


--> также добавить в urls:
  path('music/', get_music),

--> settings:
    #My_apps
    'music_app',

    #Библиотеки
    'rest_framework',
--> views:
return Response(musics)
будет ошибка -- требует Json формат--> создаем serializers.py
class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

--> views:
@api_view(['GET'])  --- получить всю информацию, через ДЕКОРАТОР
def get_music(request):

    musics = Music.objects.all()  --- object метод (получения инфо) и получить всю инф-ю как QuerySet

    print(musics)
    serializer = MusicSerializer(musics, many=True) --- Serializer возвращает JSON

    return Response(serializer.data)  ---> Возвращает JSON формат--> этот формат берет Фронтендщик JS, и связывает для правильного отображения

>>>>>******
В браузере -- Мы клиент, отправляем запрос.
Пагинация -- вывод в браузере по определен кол-ву элементов на кажд странице (ассортимент).


Запросы -- делается в Джанго через QuerySet

Джанго умеет:
Понимает ПИтон, Проводит СЕриалайзер, и выводит QueySet (вывод из БД данных),--> вывод в конце в JSON формате.


>>>>Напишем получение инфо по детально с кажд музыки
@api_view(['GET'])
def music_detail(request, id):
    music = Music.object.get(id=id)
    print(music)


--> urls:
    path('music/<int:id>/'),   (id --название должно совпадать с id в мusic_detail)

--> views:
   try:
        music = Music.objects.get(id=id)
        print(music)
        serializer = MusicSerializer(music, many=False)   -- False чтоб вывел только одну
        return Response(serializer.data)
   except Music.DoesNotExist:
        raise Http404  -- Ошибка не найден, чтоб вывел, в случае отсутствия id. импортнуть

--> Создадим Создание Музыки:
--> urls:
   path('music/create/', music_create)

--> views:
@api_view(['POST'])
def music_create(request):
    print('=========')
    print(request.data)
    print('=========')
    print(dir(request))
    serializer = MusicSerializer(data=request.data)

--> views:
def music_create(request):

    serializer = MusicSerializer(data=request.data)  -- Десериализация из JSON обратно для понятия БД
    if serializer.is_valid():   -- Если ок существует
        serializer.save() -- сохранить
        return Response(serializer.data, status=status.HTTP_201_CREATED)  -- сохранение
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) -- иначе ошибка плохой запрос

--> Можно через сайт написать ввод в JSON Формате:
{'title': 'music3', 'country': 'KG', 'category': 1 (айдишка)}  -- ОК -- HTTP 201
Если иначе -- выдаст HTTP 400

===> Postman:  (удобней)
указать локалхост
добавить поля для добавления
И также добавит
{'title': 'music3', 'country': 'KG', 'category': 1 }

--> views:  (Напишем упрощенную вывод инфо и сериализация, на автомате все включено, что сверху)
class MusicListView(ListAPIView):  -- Класс вывода (аналог сверху)
    queryset = Music.objects.all()  -- набор данных из таблицы
    serializer_class = MusicSerializer -- Сериализовать

class MusicCreateView(CreateAPIView):  -- Класс создания
    serializer_class = MusicSerializer

class MusicUpdateView(CreateAPIView):  -- Изменение добавленных
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

class MusicDetailView(RetrieveAPIView):  -- Просмотр детально
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

class MusicDeleteView(DestroyAPIView):  -- класс Удаление музыки
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


---> urls:
Поменять импорт для всех * из music_app

--> В Postman:
попробовать изменить или удалить -- но не будет, обычно принимает pk (primary key)
можно изменить так:
   lookup_field = 'id'

   либо везде, прописать url -- рк

Изменение Музыки:
PUT -- изменить все поля
PATCH -- изменить выборочно поля


--> seiralisers:

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

        # fields = ('title')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)

        category = CategorySerializer(Category.objects.get(music=instance.id)).data
        print(category)
        representation['category'] = category

        return representation

--> ДЛя каждого проекта надо создавать отдельный urls
внутри папки music_app создать urls.py (вырезать остальные с главного urls, оставить админку в главном):
from django.urls import path

from music_app.views import *

urlpatterns = [
path('music/', MusicListView.as_view()),
path('music/create/', MusicCreateView.as_view()),
path('music_update/<int:pk>/', MusicUpdateView.as_view()),
path('music_detail/<int:pk>/', MusicDetailView.as_view()),
path('music_delete/<int:pk>/', MusicDeleteView.as_view()),
    ]

---> В main urls добавить, котор перенаправляет в music_app urls:
    path('music/', include('music_app.urls'))


--> Теперь запросы в Postman:  (через дополнительн путь music/ - поскольку указали в пусть)
 http://localhost:8000/music/music_detail/6


---> Github


"""
