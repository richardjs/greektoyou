from django.http import HttpResponse
from django.shortcuts import render

from greektoyou.data import books


def read(req, book_id):
    book_id = book_id.title()
    book = books[book_id]
    return render(req, 'greektoyou/read.html', locals())
