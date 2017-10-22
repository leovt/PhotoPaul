from django.db import models
from django.db.models import F
from django.utils.encoding import python_2_unicode_compatible
from PIL import Image
from PIL.Image import ROTATE_90, ROTATE_270

@python_2_unicode_compatible
class Project(models.Model):
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def ordered_elements(self):
        return iter(self.element_set.order_by('order'))
            
    def insert_element(self, after, type):
        assert type in (Element.TEXT, Element.PHOTO)
        if after is None:
            after_order = 0
        else:
            after_order = after.order

        for el in self.element_set.filter(order__gt=after_order).order_by('-order'):
            el.order += 1
            el.save()

        el = Element(project=self, type=type, order=after_order+1)
        if el.type == Element.TEXT:
            el.text = ''
        el.save()

        return el
        
    
@python_2_unicode_compatible
class Photo(models.Model):
    date_taken = models.DateTimeField()
    image = models.ImageField(upload_to='photo_uploads/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.image.name
    
    def rotate_ccw(self):
        im = Image.open(self.image.path)
        im.transpose(ROTATE_90).save(self.image.path)
    
    def rotate_cw(self):
        im = Image.open(self.image.path)
        im.transpose(ROTATE_270).save(self.image.path)
    
@python_2_unicode_compatible
class Element(models.Model):
    TEXT = 'T'
    PHOTO = 'P'
    _CHOICES = ((TEXT, 'Text'),
                (PHOTO, 'Photo'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    #next = models.OneToOneField('self', null=True, blank=True, related_name='prev', on_delete=models.SET_NULL)
    type = models.CharField(max_length=1, choices=_CHOICES)
    photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(null=True, blank=True)
    order = models.IntegerField()
    
    class Meta:
        unique_together = (('project', 'order'),
                           )
    def __str__(self):
        if self.type == Element.TEXT:
            return (self.text or '')[:15]  + ' ...'
        elif self.type == Element.PHOTO:
            return 'Photo: %s' % self.photo