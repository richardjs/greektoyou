import logging
import os

from xml.etree import ElementTree

class Book:
    def __init__(self, title):
        self.title = title
        self.paragraphs = []

class Paragraph:
    def __init__(self):
        self.sentences = []

    def words(self):
        for sentence in self.sentences:
            for word in sentence:
                yield word

class Sentence:
    def __init__(self):
        self.words = []

    def __str__(self):
        return ' '.join([word.word for word in self.words])

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        yield from self.words

class Word:
    def __init__(self, text, prefix, verse):
        self.text = text
        self.prefix = prefix
        self.suffix = ''
        self.verse = verse

#    def __init__(self, lemma, text, word, form, number):
#        self.lemma = lemma
#        self.word = text
#        self.text = word
#        self.form = form
#        self.number = number

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()

print('Loading sblgnt.xml...')
books = {}
xml = ElementTree.parse(os.path.join('data', 'sblgnt.xml'))
for book_el in xml.findall('book'):
    book = Book(book_el.find('title').text)

    verse = None
    for p_el in book_el.findall('p'):
        paragraph = Paragraph()
        book.paragraphs.append(paragraph)

        sentence = Sentence()
        word = None
        prefix = ''
        for child in p_el:
            if child.tag == 'verse-number':
                verse = child.attrib['id']
            elif child.tag == 'prefix':
                prefix = child.text
            elif child.tag == 'w':
                sentence.words.append(Word(child.text, prefix, verse))
                prefix = ''
            elif child.tag == 'suffix':
                sentence.words[-1].suffix = child.text
                if '.' in child.text or ';' in child.text:
                    paragraph.sentences.append(sentence)
                    sentence = Sentence()

    books[book_el.attrib['id']] = book

print('Done! %d books loaded.' % len(books))
