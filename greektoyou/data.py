import logging
import os
import unicodedata
from functools import lru_cache
from xml.etree import ElementTree


@lru_cache()
def pos_string(pos):
    return {
        'A-': 'adjective',
        'C-': 'conjunction',
        'D-': 'adverb',
        'I-': 'interjection',
        'N-': 'noun',
        'P-': 'preposition',
        'RA': 'definite article',
        'RD': 'demonstrative pronoun',
        'RI': 'interrogative/indefinite pronoun',
        'RP': 'personal pronoun',
        'RR': 'relative pronoun',
        'V-': 'verb',
        'X-': 'particle',
    }[pos]


@lru_cache()
def parse_string(parse):
    s = ''
    s += {'1': '1st person ', '2': '2nd person ',
          '3': '3rd person '}.get(parse[0], '')
    s += {'P': 'present ', 'I': 'imperfect ', 'F': 'future ',
          'A': 'aorist ', 'X': 'perfect ', 'Y': 'pluperfect '}.get(parse[1], '')
    s += {'A': 'active ', 'M': 'middle ', 'P': 'passive '}.get(parse[2], '')
    s += {'I': 'indicative ', 'D': 'imperative ', 'S': 'subjunctive ',
          'O': 'optative ', 'N': 'infinitive ', 'P': 'participle '}.get(parse[3], '')
    s += {'N': 'nominative ', 'G': 'genitive ',
          'D': 'dative ', 'A': 'accusative '}.get(parse[4], '')
    s += {'S': 'singular ', 'P': 'plural '}.get(parse[5], '')
    s += {'M': 'masculine ', 'F': 'feminine ',
          'N': 'neuter '}.get(parse[6], '')
    s += {'C': 'comparative ', 'S': 'superlative '}.get(parse[7], '')
    return s


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
    def __init__(self, number):
        self.number = number
        self.words = []

    def __str__(self):
        return ' '.join([word.word for word in self.words])

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        yield from self.words


class Word:
    def __init__(self, code, text, lemma, pos, parse, prefix, verse):
        self.code = code
        self.text = text
        self.lemma = lemma
        self.pos = pos_string(pos)
        self.parse = parse_string(parse)
        self.prefix = prefix
        self.suffix = ''
        self.verse = verse

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()


morphgnt_dir = os.path.join('data', 'morphgnt-sblgnt')
morphgnt_filenames = [os.path.join(morphgnt_dir, f)
                      for f in sorted(os.listdir(morphgnt_dir))]

print('Loading sblgnt and morphgnt...')
BOOKS = {}
WORDS = {}
sbl_xml = ElementTree.parse(os.path.join('data', 'sblgnt.xml'))
for book_el in sbl_xml.findall('book'):
    book = Book(book_el.find('title').text)
    book_id = book_el.attrib['id'].lower()

    morphgnt = open(morphgnt_filenames.pop(0))

    sentence_number = 0
    word_count = 0
    verse = None
    sentence = Sentence(sentence_number)
    sentence_number += 1
    for p_el in book_el.findall('p'):
        paragraph = Paragraph()
        book.paragraphs.append(paragraph)

        prefix = ''
        for child in p_el:
            if child.tag == 'verse-number':
                verse = child.attrib['id']
            elif child.tag == 'prefix':
                prefix = child.text
            elif child.tag == 'w':
                _, pos, parse, _, _, _, lemma = morphgnt.readline().split()
                code = book_id.lower() + str(word_count)
                word_count += 1

                word = Word(code, child.text, lemma, pos, parse, prefix, verse)

                sentence.words.append(word)
                WORDS[word.code] = word

                prefix = ''
            elif child.tag == 'suffix':
                sentence.words[-1].suffix = child.text
                if '.' in child.text or ';' in child.text:
                    paragraph.sentences.append(sentence)
                    sentence = Sentence(sentence_number)
                    sentence_number += 1

    BOOKS[book_id] = book

print('Done! %d books loaded.' % len(BOOKS))

print('Loading strongs...')

DEFINITIONS = {}
strongs_xml = ElementTree.parse(os.path.join('data', 'strongsgreek.xml'))

number_words = {}
for entry in strongs_xml.find('entries').findall('entry'):
    number = int(entry.find('strongs').text)
    try:
        word = entry.find('greek').attrib['unicode']
    except AttributeError:
        continue
    number_words[number] = word

for entry in strongs_xml.find('entries').findall('entry'):
    try:
        word = entry.find('greek').attrib['unicode']
        word = unicodedata.normalize('NFC', word)

        # special case
        # if word == 'τὶς':
        #    word = 'τις'

    except AttributeError as e:
        continue
    definition_e = entry.find('strongs_def')
    if definition_e == None:
        definition_e = entry.find('strongs_derivation')
    if definition_e == None:
        continue

    number = int(entry.find('strongs').text)
    definition = ''
    for e in definition_e.iter():
        if e.text:
            definition += e.text

        if e.tag == 'strongsref':
            if e.attrib['language'] == 'GREEK':
                definition += number_words[int(e.attrib['strongs'])]
            else:
                definition += '#%d' % (int(e.attrib['strongs']))
        elif e.tag == 'greek':
            definition += e.attrib['unicode']

        if e.tail:
            definition += e.tail

    definition = definition.replace('\n', '')

    DEFINITIONS[word] = definition

print('Done!')
