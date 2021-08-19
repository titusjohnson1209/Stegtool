from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import time
import os.path
from . import steg as lsbsteg
from . import filesteg as lsbfilesteg


UPLOAD_ROOT = os.path.dirname(os.path.realpath(__name__))

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def encode(request):
    return render(request, 'encode.html', {})


def process_encoding_data(request):
    if request.method == 'POST' and request.FILES['coverimage']:
        coverimage = upload_file(request.FILES['coverimage'])
        if request.POST.get('istextsteg'):
            message = request.POST.get('message')
            stegImage = encode_image_text_steg(message, coverimage)
            return JsonResponse(status=200, data={'status': 'true', 'location': '../' + stegImage})

        else:
            textstegfile = upload_file(request.FILES['textfile'])
            stegImage = encode_image_text_file_steg(textstegfile, coverimage)
            return JsonResponse(status=200, data={'status': 'true', 'location': '../' + stegImage})
    if request.method == 'GET':
        return HttpResponseNotFound('<h1>Not Allowed</h1>')

def encode_image_text_steg(message, coverimg):
    if message == '':
        message = 'no text found'
    if coverimg is not None:
        newImg = lsbsteg.encodeLSB(message, UPLOAD_ROOT + coverimg)
        if not newImg is None:
            return newImg
        else:
            return


def encode_image_text_file_steg(textfile, coverimg):
    if coverimg is not None and textfile is not None:
        newImg = lsbfilesteg.encodeLSB(UPLOAD_ROOT + textfile, UPLOAD_ROOT + coverimg)
        if not newImg is None:
            return newImg
        else:
            return


def decode(request):
    return render(request, 'decode.html', {})


def process_decoding_data(request):
    if request.method == 'POST' and request.FILES['stegimage']:
        steg_image = upload_file(request.FILES['stegimage'])
        if request.POST.get('istextsteg'):
            messageDecoded = decode_text_from_image(steg_image)
            return JsonResponse(status=200, data={'status': 'true', 'message': messageDecoded})

        else:
            textfile = decode_textfile_from_image(steg_image)
            return JsonResponse(status=200, data={'status': 'true', 'location': '../' + textfile})
    if request.method == 'GET':
        return HttpResponseNotFound('<h1>Not Allowed</h1>')


def decode_text_from_image(steg_image):
    if steg_image is not None:
        message_decoded = lsbsteg.decodeLSB(UPLOAD_ROOT + steg_image)
        if not message_decoded is None:
            return message_decoded
        else:
            return



def decode_textfile_from_image(steg_image):
    textFile = lsbfilesteg.decodeLSB(UPLOAD_ROOT + steg_image)
    if not textFile is None:
        return textFile
    else:
        return


def upload_file(my_file):
    if my_file is not None:
        fs = FileSystemStorage()
        extension = os.path.splitext(my_file.name)[1]
        filename = fs.save(time_in_millisecond() + extension, my_file)
        uploaded_file_url = fs.url(filename)
        return uploaded_file_url
    else:
        return None


def time_in_millisecond():
    millis = int(round(time.time() * 1000))
    return str(millis)
 