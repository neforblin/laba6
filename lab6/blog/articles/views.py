from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


# Create your views here.
def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    # get one exact view
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404


def create_post(request):
    if not request.user.is_anonymous:

        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"].strip()
            }

            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок + проверка уникальности
                unic = Article.objects.filter(title=form["title"])

                if not unic:
                    article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id=article.id)
                else:
                    form['errors'] = u"Такая статья уже есть!"
                    return render(request, 'newpost.html', {'form': form})

            # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'newpost.html', {'form': form})

        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'newpost.html', {})

    else:
        raise Http404


def register_user(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            if request.POST["username"]and request.POST["email"] and request.POST["password"]:

                form = {
                    'username': request.POST["username"],
                    'email': request.POST["email"],
                    'password': request.POST["password"],
                }
                if form["username"] == '' or form["email"] == ''  or form["password"] == '' :
                    form['errors'] = u"вы отправили пустую строку в одно из полей"
                    return render(request, 'register.html', {'form': form})

                if_username_unique = User.objects.filter(username=form["username"])
                if_email_unique = User.objects.filter(email=form["email"])

                if len(if_username_unique) == 0 and len(if_email_unique) == 0:
                    article = User.objects.create_user(form["username"], form["email"], form["password"])
                    return redirect("../login/")


                else:
                    form['errors'] = u"Не уникальный юзернейм/почта"
                    return render(request, 'register.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'register.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'register.html', {})
    else:
        raise Http404


def login_user(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'username': request.POST["username"],
                 'password': request.POST["password"],
            }
            if form["username"] and form["password"]:
                if form["username"] == '' or form["password"] == '' :
                    form['errors'] = u"вы отправили пустую строку в одно из полей"
                    return render(request, 'login.html', {'form': form})

                user = authenticate(username=form["username"], password=form["password"])

                if user:
                    form['errors'] = u"Вы успешно вошли!"
                    login(request, user)
                    return render(request, 'login.html', {'form': form})
                else:
                    form['errors'] = u"Не правильный пароль или логин"
                    return render(request, 'login.html', {'form': form})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'login.html', {'form': form})
        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'login.html', {})
    else:
        return render(request, 'archive.html', {})