#coding: utf-8
import multiprocessing
import re
import concurrent.futures

__author__ = 'erofeev'


class Shingler:
    source_text = None
    shingle_size = None
    shingles = None
    lock = None

    def __init__(self, text, size):
        self.source_text = text
        self.shingle_size = size
        self.shingles = set()
        self.lock = multiprocessing.Lock()

    def fill_shingles_by_parts(self):
        cpu_count = multiprocessing.cpu_count()
        with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count) as executor:
            future_to_url = list()
            for text_part in re.split('[:!?.,]', self.source_text): #TODO don't remove urls!!
                text_part = text_part.strip()
                future_to_url.append(executor.submit(self.split_shingles_by_words, text_part))
        concurrent.futures.as_completed(future_to_url)

    def get_shingles(self):
        self.fill_shingles_by_parts()
        ret = list(shingle for shingle in self.shingles)
        ret.sort()
        return ret

    def get_int_shingles(self):
        self.fill_shingles_by_parts()
        ret = list(hash(shingle) for shingle in self.shingles)
        ret.sort()
        return ret


    def split_shingles_by_words(self, text):
        text = self.remove_excuses(text)
        words = text.split()
        self.pick_shingles(0, words)
        self.pick_shingles(self.shingle_size / 2, words)

    def pick_shingles(self, pos, words):
        shingle_words = list()
        while pos < len(words):
            shingle_words.append(words[pos])
            if len(shingle_words) % self.shingle_size == 0:
                self.prepare_and_add_shingle(shingle_words)
                shingle_words = list()
            pos += 1
        if len(shingle_words) > 0:
            self.prepare_and_add_shingle(shingle_words)


    def prepare_and_add_shingle(self, shingle_words):
        if len(shingle_words) < 2:
            return
        shingle_words.sort()
        result_shingle_words = list()
        for word in shingle_words:
            word = word.lower()
            word = self.remove_end_of_word(word)
            word = word.strip()
            if len(word) > 0:
                result_shingle_words.append(word)
        shingle = " ".join(result_shingle_words)
        shingle = shingle.encode("utf-8")
        self.lock.acquire()
        self.shingles.add(shingle)
        self.lock.release()


    def remove_end_of_word(self, src):
        for end in ends:
            if src.endswith(end):
                return src[: - len(end)]
        return src


    def remove_excuses(self, text):
        for excuse in excuses:
            text = text.replace(excuse + " ", "no")
        return text


def decode_to_utf8(strings):
    ret = list()
    for string in strings:
        ret.append(string.decode("utf-8"))
    return ret


ends = ["у", "е", "и", "ий", "ия", "ие", "мя", "а", "ях", "ая", "ить", "ать", "их", "ых", "чь", "шь", "ья", "ы",
        "ся", "ет", "ой", "ать", "ять", "им", "ось", "ет", "от", "ют", "ов", "ей", "ом"]
ends = decode_to_utf8(ends)
excuses = ['неочень', 'нет', 'не', 'врятли', 'врядли', 'вряд ли', 'eдва ли', 'навряд ли', 'сомнительно',
           "nope", 'no', "редко", "никогда"]
excuses = decode_to_utf8(excuses)