import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_luotu_paate_on_olemassa(self):
        self.assertNotEqual(self.kassapaate, None)

    def test_konstruktori_asettaa_pohjakassan_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_konstruktori_asettaa_myydyt_lounaat_oikein(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisosto_toimii_edullisille_kun_maksu_ok(self):
        self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)

    def test_kateisosto_toimii_oikein_edullisille_kun_maksu_ei_riita(self):
        self.kassapaate.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)

    def test_kateisosto_toimii_maukkaille_kun_maksu_ok(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

    def test_kateisosto_toimii_oikein_maukkaille_kun_maksu_ei_riita(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)

        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(200), 200)

    def test_korttiosto_toimii_edullisille_kun_maksu_ok(self):

        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)
        self.assertEqual(self.maksukortti.saldo_euroina(), 7.6)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_korttiosto_toimii_oikein_edullisille_kun_maksu_ei_riita(self):
        self.maksukortti.ota_rahaa(800)

        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), False)
        self.assertEqual(self.maksukortti.saldo_euroina(), 2)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_korttiosto_toimii_maukkaille_kun_maksu_ok(self):

        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)
        self.assertEqual(self.maksukortti.saldo_euroina(), 6)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_korttiosto_toimii_oikein_maukkaille_kun_maksu_ei_riita(self): 
        self.maksukortti.ota_rahaa(800)

        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), False)
        self.assertEqual(self.maksukortti.saldo_euroina(), 2)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kortin_lataus_kasvattaa_saldoa_ja_kassaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)

        self.assertEqual(self.maksukortti.saldo_euroina(), 11)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)

    def test_kortin_lataus_kasvattaa_saldoa_ja_kassaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1000)

        self.assertEqual(self.maksukortti.saldo_euroina(), 10)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)