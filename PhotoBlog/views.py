from django.shortcuts import render, get_object_or_404
from .models import Project, Element
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.urls.base import reverse
from django.views import View

# Create your views here.
def gallery(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'PhotoBlog/gallery.html', {'project': project})

# Create your views here.
def blog(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'PhotoBlog/blog.html', {'project': project})

# Create your views here.
def editor(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'PhotoBlog/editor.html', {'project': project})
    
def element(request, element_id):
    element = get_object_or_404(Element, id=element_id)
    project = element.project
    anchor = ''
    if request.POST['action'] == 'delete':
        element.delete()
    elif request.POST['action'] == 'text_update':
        if element.type != Element.TEXT:
            return HttpResponseBadRequest("need to specify valid action")
        element.text = request.POST.get('text', '')
        element.save()    
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