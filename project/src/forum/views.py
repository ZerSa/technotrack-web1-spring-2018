# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseForbidden
from .models import Topic
from django import forms
from django.views.generic import UpdateView, CreateView


class TopicListForm(forms.Form):
    sort = forms.ChoiceField(choices=(
        ('name', 'name asc'),
        ('-name', 'name desc'),
        ('author', 'author')
    ), required=False)
    search = forms.CharField(required=False)


class TopicEdit(UpdateView):
    model = Topic
    fields = 'name',
    context_object_name = 'topics'
    template_name = 'topic_edit.html'

    def get_success_url(self):
        return reverse('topic_detail', kwargs={'pk': self.object.pk})


class TopicCreate(CreateView):
    model = Topic
    fields = 'name',
    context_object_name = 'topics'
    template_name = 'topic_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TopicCreate, self).form_valid(form)


    def get_success_url(self):
        return reverse('topic_detail', kwargs={'pk': self.object.pk})


def topic_list(request):
    topics = Topic.objects.all()
    form = TopicListForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data
        if data['sort']:
            topics = topics.order_by(data['sort'])
        if data['search']:
            topics = topics.filter(name=data['search'])

    context = {
        'topics': topics,
        'topics_form': form
    }
    return render(request, 'topic_list.html', context)


def topic_create(request):
    topic = Topic(author=request.user)
    if request.method == 'GET':
        form = TopicForm(instance=topic)
        return render(request, 'topic_create.html', {'form': form})
    elif request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            topic = form.save()
            return redirect('topic_detail', pk=topic.id)
        else:
            return render(request, 'topic_create.html', {'form': form})


def topic_detail(request, pk):
    context = {
        'topics': get_object_or_404(Topic, id=pk)
    }
    return render(request, 'topic_detail.html', context)



