import json

from django.http import JsonResponse
from django.shortcuts import render

from greektoyou import data, models


def read(req, book_id):
    book_id = book_id.lower()
    book = data.BOOKS[book_id]
    # TODO use logged in user here
    # TODO need an action/default if no progress
    # TODO read based on progress ID, in case of multiple progresses?
    book_progress = models.BookProgress.objects.filter(book=book_id)[0]
    return render(req, 'greektoyou/read.html', locals())


def api_info(req, word_code):
    info = dict(data.WORDS[word_code].__dict__)

    # these fields aren't needed by the front-end
    del info['code']
    del info['text']
    del info['prefix']
    del info['suffix']

    info['definition'] = data.DEFINITIONS.get(
        info['lemma'], 'Definition not found!')

    return JsonResponse(info)
