from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Assignment, Course, Module, ToDoList, Discussion, DiscussionReply
from .forms import  CreateAssignment, CreateCourse, CreateDiscussionPost,CreateDiscussionPostReply, CreateModule, CreateNewList
from django.utils import timezone

# Create your views here.

def assignment(response, id):
    asmt = Assignment.objects.get(id=id)
    return render(response, "main/assignment.html", {"asmt": asmt})

def assignments(response):
    if response.method == "POST":
        print(response.POST)
        form = CreateAssignment(response.POST)
        if form.is_valid():
            
            title = form.cleaned_data["title"]
            max_grade_pts = form.cleaned_data["max_grade_pts"]
            description = form.cleaned_data["description"]
            course = Course(id=response.session['current_course_id'])

            a = Assignment(title=title, max_grade_pts=max_grade_pts, description=description, course=course)
            a.save()
    else:
        form = CreateAssignment()

    assignments = Assignment.objects.all()
    current_course = response.session['current_course_id']
    course_asmt_count = 0
    course_has_asmts = False

    for assignment in assignments:
        if int(assignment.course.id) == int(current_course):
            course_asmt_count += 1

    if course_asmt_count != 0:
        course_has_asmts = True

    return render(response, "main/assignments.html", {"assignments": assignments, "course_has_asmts": course_has_asmts})

def list(response, id):
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
    return render(response, "main/tdl.html", {"ls": ls})

def home(response):
    return render(response, "main/home.html", {})

def courses(response):
    if response.method == "POST":
        if 'addCourse' in response.POST:
            form = CreateCourse(response.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]

                c = Course(title=title)
                c.save()
                response.user.teacherscourse.add(c)

                return HttpResponseRedirect("/courses")
        elif 'changeCurrentCourse' in response.POST:
            response.session['current_course'] = response.POST['changeCurrentCourse']
            response.session['current_course_id'] = response.POST['courseId']
            print(response.POST)

    current_course = response.session.get('current_course')
    current_course_id = response.session.get('current_course_id')
    
    if current_course is None:
        current_course = 'None'
 
    if current_course_id is None:
        current_course_id = 0

    response.session['current_course'] = current_course
    response.session['current_course_id'] = current_course_id

    return render(response, "main/courses.html", {"teacherscourse": response.user.teacherscourse})

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
    if response.method == "POST":
        form = CreateModule(response.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            #courseId = form.cleaned_data["course"]
            course = Course(id=response.session['current_course_id'])

            m = Module(title=title, course=course)
            m.save()
            response.user.teachersmodule.add(m)

    else:
        form = CreateModule()

    return render(response, "main/modules.html", {"teacherscourse": response.user.teacherscourse, "teachersmodule": response.user.teachersmodule})

def tdl(response):
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

    return render(response, "main/tdl.html", {"form": form})