import datetime
import requests as requests
from bs4 import BeautifulSoup

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView

from .forms import LoginForm, CommentAdd
from .models import News, CustomUser, Comment


def main(request):
    """Main page"""
    context = {
        'user_id': request.user.pk
    }
    return render(request, 'store/index.html', context)

def news(request):
    """Last news"""
    context = {
        'last_news': News.objects.all(),
        'user_id': request.user.pk
    }
    return render(request, 'store/generic.html', context)

class NewsDetailView(DetailView, FormView):
    """Detail news page"""
    model = News
    form_class = CommentAdd

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = CustomUser.objects.filter(id=self.request.user.pk)
        context['comment'] = Comment.objects.filter(post_news=self.get_object().pk)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print(1111)
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        print(self.object.slug)
        comment = dict()
        comment['post_news'] = News.objects.get(id=self.object.pk)
        comment['comment'] = form.cleaned_data['comment']
        comment['date'] = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')
        comment['author'] = CustomUser.objects.get(id=self.request.user.pk)
        Comment.objects.create(post_news=comment['post_news'],
                               comment=comment['comment'],
                               date=comment['date'],
                               author=comment['author'])
        return redirect('news_detail', self.object.slug)

    def form_invalid(self, form):
        return redirect('news_detail', self.object.slug)

def user_login(request):
    if request.method == 'POST' and request.user.pk != 'None':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('main')
                else:
                    print('Disabled account')
                    return HttpResponse('Disabled account')
            else:
                print('Invalid login')
                return HttpResponse('Invalid login')

    context = {
        'form': LoginForm(),
        'user_id': request.user.pk
    }
    if request.user.pk != 'None':
        return redirect('main')
    return render(request, 'store/login.html', context)

def user_profile(request):
    user = CustomUser.objects.filter(id=request.user.pk).first()
    context = {
        'user': user,
        'user_id': request.user.pk,
        'comment': Comment.objects.filter(author=user),
    }
    if context['user'] == None or context['user_id'] == None:
        return redirect('user_login')
    return render(request, 'store/profile.html', context)

def turnament_view():
    url = 'https://www.cybersport.ru/base/tournaments?sort=start&filterOrder=auto&status=future&page=1'
    session = requests.Session()
    page = session.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    all_future_tourneer = soup.find('section', class_='tournaments').findAll('li', class_='tournaments__item tournament')
    list_turnament = []
    for element in all_future_tourneer:
        list_turnament.append([
            element.find('div', class_='tournament__name').text.strip(),
            element.find('div', class_='tournament__date').text.strip(),
            element.find('div', class_='tournament__fund').text.strip(),
            element.find('div', class_='tournament__game').find('i').get('class'),
                      ])
    return list_turnament