from django.shortcuts import render, get_object_or_404
from .models import Project, Element, Photo
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.urls.base import reverse
from django.utils.html import escape
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import get_user
from django.contrib.auth.views import redirect_to_login

# Create your views here.
def gallery(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if not get_user(request).is_authenticated and not project.is_public:
        return redirect_to_login(request.get_full_path())    
      
    return render(request, 'PhotoBlog/gallery.html', {'project': project})

# Create your views here.
def blog(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if not get_user(request).is_authenticated and not project.is_public:
        return redirect_to_login(request.get_full_path())    
      
    return render(request, 'PhotoBlog/blog.html', {'project': project})

def bloglist(request):
    if get_user(request).is_authenticated:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(is_public=True)
    return render(request, 'PhotoBlog/list.html', {'projects': projects})

@login_required
def editor(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'GET':
        return render(request, 'PhotoBlog/editor.html', {'project': project})
    if request.method == "POST":
        project.name = request.POST['name']
        project.is_public = int(request.POST['is_public'])
        project.save()
        return HttpResponseRedirect(reverse('PhotoBlog:editor', args=(project.id,)))
        
    
@login_required
def element(request, element_id):
    element = get_object_or_404(Element, id=element_id)
    project = element.project
    anchor = '#el%d' % element.id
    if request.POST['action'] == 'delete':
        anchor = ''
        element.delete()
    elif request.POST['action'].startswith('text_update'):
        if element.type != Element.TEXT:
            return HttpResponseBadRequest("need to specify valid action")
        element.text = request.POST.get('text', '')
        element.save()    
        if request.POST['action'] == 'text_update_ajax':
            return HttpResponse(status=204)
    elif request.POST['action'] == ('rotate_cw'):
        if element.type != Element.PHOTO:
            return HttpResponseBadRequest("need to specify valid action")
        element.photo.rotate_cw()
    elif request.POST['action'] == ('rotate_ccw'):
        if element.type != Element.PHOTO:
            return HttpResponseBadRequest("need to specify valid action")
        element.photo.rotate_ccw()
    elif request.POST['action'].startswith('photo_update:'):
        if element.type != Element.PHOTO:
            return HttpResponseBadRequest("need to specify valid action")
        photo_id = request.POST['action'][13:]
        photo = element.project.photo_set.get(id=photo_id)
        if not photo:
            return HttpResponseBadRequest("need to specify valid photo")
        element.photo = photo
        element.save()
    else:
        return HttpResponseBadRequest("need to specify valid action")

    return HttpResponseRedirect(reverse('PhotoBlog:editor', args=(project.id,)) + anchor)


@login_required
def insert(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    after_id = request.POST.get('after', None)
    if after_id is None:
        after=None
    else:
        try:
            after = project.element_set.get(id=after_id)
        except Element.DoesNotExist:
            return HttpResponseBadRequest("referneced element not found")
    try:
        type = {'P':'P', 'T':'T'}[request.POST['type']]
    except KeyError:
        return HttpResponseBadRequest("need to specify valid type")
    el = project.insert_element(after=after, type=type)
    
    return HttpResponseRedirect('%s#el%d' % (reverse('PhotoBlog:editor', args=(project.id,)), el.id))

@login_required
def upload(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'GET':
        return render(request, 'PhotoBlog/upload.html', {'project': project})
    if request.method == "POST":
        photos = []
        for image in request.FILES.getlist("images"):
            ph = Photo(project=project, image=(image))
            ph.date_taken = timezone.now()
            ph.save()
            photos.append((ph, len(image)))
        return HttpResponse(escape(repr(photos)))

def create(request):
    if request.method == 'GET':
        return render(request, 'PhotoBlog/create.html')
    if request.method == "POST":
        project = Project(name=request.POST['name'])
        project.save()
        return HttpResponseRedirect(reverse('PhotoBlog:upload', args=(project.id,)))
        
    