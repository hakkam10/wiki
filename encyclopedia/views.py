from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import markdown2
from markdown2 import Markdown

from . import util

class EditEntry(forms.Form):
    content = forms.CharField(label="content", widget=forms.Textarea)

class NewEntry(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class':'form-control'})) 
    content = forms.CharField(label="content", widget=forms.Textarea)
   


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, title):
    markdowner = Markdown()
    try:
        return render(request, "encyclopedia/content.html", {
        "entry": markdowner.convert(util.get_entry(title)),
        "title": title
    })
    except TypeError:
        return render(request, "encyclopedia/content.html", {
        "entry": "Page does not exist",
        "title": "Error"
    })

def edit(request, title):
    if request.method == "POST":
        entry = EditEntry(request.POST)
        if entry.is_valid():
            content = entry.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:content", args=(title,)))
        else:
            return render(request, "encyclopedia/edit.html", {
            "message":"Error",
            "title":title,
            "form":entry
            })
    else:
        return render(request, "encyclopedia/edit.html", {
        "title":title,
        "content":util.get_entry(title),
        "form":EditEntry(initial={"title":title, "content":util.get_entry(title)})
        })
    
def new(request):
    if request.method == "POST":
        entry = NewEntry(request.POST)
        if entry.is_valid():
            title = entry.cleaned_data['title']
            content = entry.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:content", args=(title,)))
        else:
            return render(request, "encyclopedia/new.html", {
            "form":entry
        })
    else:
        return render(request, "encyclopedia/new.html", {
            "form":NewEntry()
        })

