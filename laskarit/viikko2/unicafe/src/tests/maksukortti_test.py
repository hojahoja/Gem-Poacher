import unittest
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(500)

        self.assertEqual(self.maksukortti.saldo_euroina(), 15.0)

    def saldo_vahenee_oikein_jos_rahaa_on_tarpeeksi(self):
        self.maksukortti.ota_rahaa(300)

        self.assertEqual(self.maksukortti.saldo_euroina(), 7.0)

    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1300)

        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_metodi_palauttaa_True_jos_rahat_riittivat(self):
        self.assertEqual(self.maksukortti.ota_rahaa(900), True)

    def test_metodi_palauttaa_False_jos_rahat_eivat_riita(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1900), False)

    def test_str_metodi_ilmoittaa_saldon_oikein(self):
        odotettu = "Kortilla on rahaa 10.00 euroa"
        self.assertEqual(str(self.maksukortti), odotettu)
