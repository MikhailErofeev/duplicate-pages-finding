# -*- coding: utf-8 -*-
import unittest
from bs4 import BeautifulSoup
from src import text_processing
from src.shingles import Shingler
from src.hashes import get_similarity, get_document_lsh_keys
from src.document import Document


__author__ = 'erofeev'


class Tests(unittest.TestCase):
    def test_get_main_text_from_html(self):
        ret = text_processing.get_main_text_from_probably_html(
            text_processing.get_text_from_file("../data/Владимир Путин собирается в Гатчину.html"))
        expect = "30 апреля в Петербургском институте ядерной физики им. Б.П. Константинова " \
                 "Национального исследовательского центра «Курчатовский институт» состоится заседание " \
                 "Совета при Президенте Российской Федерации по науке и образованию. " \
                 "На нём планируется обсудить вопросы формирования и развития современной инфраструктуры " \
                 "научных исследований в России, а также совершенствования оценки результативности деятельности " \
                 "научных организаций. Председательствовать на заседании Совета будет " \
                 "Президент РФ Владимир Путин. Фото: echo.msk.ru".decode('utf-8')
        self.assertEqual(expect, ret)
        ret = text_processing.get_main_text_from_probably_html(
            text_processing.get_text_from_file(
                "../data/Супертурер CUBE KATHMANDU   Обзоры велосипедов   CUBE Russia.html"))
        expect = "Благородная однотонная внешность, чрезвычайно прочная даже на вид рама со стойким к царапинам " \
                 "анодированием — очень приятный байк. Тем более радует, что и ездить на нем тоже очень приятно. " \
                 "Руки уверенно хватаются за удобный, 700-миллимитровый руль Syntace, посадка же на " \
                 "эргономически выверенном седле обеспечивает идеальное сочетание спортивности и комфорта. " \
                 "Очевидно, что этот байк проектировали для дальних поездок, и все получилось как надо. " \
                 "Воздушная вилка вполне комфортна и функциональна: в распоряжении велосипедиста имеется " \
                 "манетка блокировки — полезная вещь при движении, скажем, по горному серпантину вверх. " \
                 "Практичности байку добавляет высокоуровневое оборудование Shimano, полноразмерные крылья, " \
                 "светотехника и внутренняя прокладка рубашек тросиков: шанс случайно повредить один из них минимален." \
                 " Стоит назвать хорошим выбором и ободную гидравлику Magura — неубиваемые тормоза, " \
                 "проверенные временем и тысячами туристических километров. РЕЗЮМЕ: на примере KATHMANDU " \
                 "можно смело делать вывод о всем семействе туристических велосипедов CUBE: это в " \
                 "высшей степени продуманные, удобные, добротные и качественные байки, готовые к " \
                 "туристическим заездам любой протяженности. Единственным минусом семейства являются " \
                 "ценники — CUBE KATHMANDU с со-товарищами весьма недешев. " \
                 "Для добавления комментариев требуется авторизация.".decode('utf-8')
        self.assertEqual(expect, ret)

    def test_get_shingles(self):
        text = "найдена неочень замечательная жёлтая подводная лодка в степях Украины, не звонить по телефону 123" \
            .decode("utf-8")
        ret = Shingler(text, 4).get_shingles()
        self.assertIn("noзамечательн жёлт найден подводн", ret)
        self.assertIn("украин в лодк степ", ret)
        self.assertIn("в жёлт лодк подводн", ret)
        self.assertIn("украин степ", ret)
        self.assertIn("123 noзвон по телефон", ret)
        self.assertIn("123 телефон", ret)

    def test_min_hash(self):
        self.assertEqual(1, get_similarity(["orange", "apple"], ["apple", "orange"]))
        self.assertGreater(1, get_similarity(["orange", "apple"], ["apple"]))
        self.assertLess(0, get_similarity(["orange", "apple"], ["apple"]))

    def test_remove_empty_tags(self):
        html = """<div class="m20"><div class="right"></div>Благородная однотонная внешность</div>""".decode("utf-8")
        soup = BeautifulSoup(html)
        text_processing.remove_empty_tags(soup)
        expected = """<div class="m20"> Благородная однотонная внешность</div>""".decode("utf-8")
        real = soup.prettify().replace("\n", "")
        self.assertEqual(expected, real)

    def test_lsh(self):
        kat_text_1 = text_processing.get_main_text_from_probably_html(text_processing.get_text_from_file(
            "../data/Супертурер CUBE KATHMANDU   Обзоры велосипедов   CUBE Russia.html"))
        kat_text_2 = text_processing.get_main_text_from_probably_html(text_processing.get_text_from_file(
            "../data/сформируем велокультуру! - Супертурер CUBE KATHMANDU.html"))
        kat1 = Document(Shingler(kat_text_1, 4).get_int_shingles(), "kat1")
        kat2 = Document(Shingler(kat_text_2, 4).get_int_shingles(), "kat2")
        sim = get_similarity(kat2.shingles, kat1.shingles)
        self.assertLess(0.7, sim)
        self.assertEquals(28,
                          len(get_document_lsh_keys(30, 100, kat1).intersection(get_document_lsh_keys(30, 100, kat2))))

    def test_not_html(self):
        self.assertEqual("text text2", text_processing.get_main_text_from_probably_html("text\ntext2"))
        self.assertEqual("", text_processing.get_main_text_from_probably_html(""))


if __name__ == '__main__':
    unittest.main()