from django.contrib.auth.models import User
from django.db import models


class BookProgress(models.Model):
    '''Tracks how far a user has read through a book.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # book maps to book_id, the key of greektoyou.data.BOOKS
    book = models.CharField(max_length=4)
    # the sentence number the user is currently on
    sentence = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'BookProgresses'

    def __str__(self):
        return '%s %s %d' % (self.user, self.book, self.sentence)
