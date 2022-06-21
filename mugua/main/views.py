from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ToDoList, Discussion
from .forms import CreateNewList, CreateDiscussionPost
from django.utils import timezone

# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():
        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    
                    item.save()

            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")
        return render(response, "main/list.html", {"ls": ls})
    return render(response, "main/view.html", {"ls": ls})

def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()

    return render(response, "main/create.html", {"form": form})

def discuss(response):
    if response.method == "POST":
        form = CreateDiscussionPost(response.POST)
        #print(form)


        if form.is_valid():
            author = response.user.username
            title = form.cleaned_data["title"]
            message = form.cleaned_data["message"]
            post_date = timezone.now()

            d = Discussion(author=author, title=title, message=message, post_date=post_date)
            d.save()
        
        return HttpResponseRedirect("/discuss")
    else:
        form = CreateDiscussionPost()

    discussion = Discussion.objects.all()
    return render(response, "main/discuss.html", {"discussion": discussion})

def view(response):
    return render(response, "main/view.html", {})