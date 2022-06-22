from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ToDoList, Discussion, DiscussionReply
from .forms import CreateDiscussionPostReply, CreateNewList, CreateDiscussionPost
from django.utils import timezone

# Create your views here.

def assignments(response):
    return render(response, "main/assignments.html", {})

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

def courses(response):
    return render(response, "main/courses.html", {})

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

def view(response):
    return render(response, "main/view.html", {})

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

def discussPost(response, id):
    if response.method == "POST":
        form = CreateDiscussionPostReply(response.POST)

        if form.is_valid():
            discussion_post = Discussion.objects.get(id=id)
            author = response.user.username
            title = "RE: " + discussion_post.title
            message = form.cleaned_data["message"]
            post_date = timezone.now()

            dr = DiscussionReply(discussion=discussion_post, author=author, title=title, message=message, post_date=post_date)
            dr.save()
    else:
        form = CreateDiscussionPostReply()


    discussion_post = Discussion.objects.get(id=id)
    discussion_post_reply = DiscussionReply.objects.all() # get(discussion=id)
    return render(response, "main/discuss_post.html", {"discussion_post": discussion_post, "discussion_post_reply": discussion_post_reply})

def modules(response):
    return render(response, "main/modules.html", {})

