from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from . import util
import random
from markdown2 import markdown


def index(request):
    head='All Pages'
    return render(request, "encyclopedia/index.html", {
        "head":head,
        "entries": util.list_entries()
    })


def wikipage(request,title):
    titles = util.list_entries()
    if( title in titles):
        content=markdown(util.get_entry(title))
        return render(request,"encyclopedia/title.html",{
            "title":title,
            "content":content
        })
    else:
        title='ERROR!'
        content='Requested Entry not found!!'
        return render(request,"encyclopedia/title.html",{
            "title":title,
            "content":content
        })

@require_http_methods(["POST"])
def search(request):
    query=request.POST.get("q")
    titles = util.list_entries()
    if(query in titles):
        return HttpResponseRedirect(reverse('wikipage',args=[query]))
    else:
        head='Search Result'
        return render(request,"encyclopedia/index.html",{
            "head":head,
            "entries":util.search_result(query)
        })


def new_entry(request):
    if (request.method=="POST"):
        title = request.POST.get("title")
        if(title.strip() == ""):
            title='ERROR!'
            content='Title Cannot be Null!!'
            return render(request,"encyclopedia/title.html",{
                "title":title,
                "content":content
            })
        elif(title.lower() in [x.lower() for x in util.list_entries()]):
            title='ERROR!'
            content='Entry Already Exists!!'
            return render(request,"encyclopedia/title.html",{
                "title":title,
                "content":content
            })
        else:
            content= request.POST.get("content")
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,'encyclopedia/NewEntry.html')


def Random_page(request):
    title=random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('wikipage',args=[title]))

def edit_entry(request,title):
    if(request.method == "POST"):
        content= request.POST.get("content")
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse('wikipage',args=[title]))
    else:
        content=util.get_entry(title)
        print(content)
        return render(request,'encyclopedia/editEntry.html',{
            "title":title,
            "content":content
        })
