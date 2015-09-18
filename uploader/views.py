# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from uploader.models import Image
from uploader.form import ImageForm


def list(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = Image(image=request.FILES['image'])
            new_image.save()

            bw_image(new_image.image.name)

            return HttpResponseRedirect(reverse('uploader.views.list'))
    else:
        form = ImageForm()

    images = Image.objects.all()

    return render_to_response(
        'uploader/list.html',
        {'images': images, 'form': form},
        context_instance=RequestContext(request)
    )

def bw_image(image_name):
    try:
        import cv2 as cv
        image = cv.imread(settings.BASE_DIR + '/media/' + image_name, 0)
        cv.imwrite(settings.BASE_DIR + '/media/' + image_name, image)
    except ImportError:
        print 'Can not find opencv2 module'
