import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(2000)

    def test_kassapaatteen_alustus_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaita_myyty(), 0)
        self.assertEqual(self.kassapaate.edullisia_myyty(), 0)

    # Edulliset kateiset
    def test_onnistunut_edullinen_kateisosto_muuttaa_rahamaaria_odotetusti(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)
        self.assertEqual(vaihtoraha, 260)

    def test_onnistunut_edullinen_kateisosto_muuttaa_myyntimaaraa_odotetusti(self):
        for _ in range(0, 3):
            self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(self.kassapaate.edullisia_myyty(), 3)

    def test_epaonnistunut_edullinen_kateisosto_ei_muuttaa_rahamaaria(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(230)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(vaihtoraha, 230)

    def test_epaonnistunut_edullinen_kateisosto_ei_muuttaa_myyntimaaraa(self):
        self.kassapaate.syo_edullisesti_kateisella(230)

        self.assertEqual(self.kassapaate.edullisia_myyty(), 0)

    # Maukkaat kateiset
    def test_onnistunut_maukas_kateisosto_muuttaa_rahamaaria_odotetusti(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.0)
        self.assertEqual(vaihtoraha, 100)

    def test_onnistunut_maukas_kateisosto_muuttaa_myyntimaaraa_odotetusti(self):
        for _ in range(0, 3):
            self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.maukkaita_myyty(), 3)

    def test_epaonnistunut_maukas_kateisosto_ei_muuttaa_rahamaaria(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(230)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(vaihtoraha, 230)

    def test_epaonnistunut_maukas_kateisosto_ei_muuttaa_myyntimaaraa(self):
        self.kassapaate.syo_maukkaasti_kateisella(230)

        self.assertEqual(self.kassapaate.maukkaita_myyty(), 0)

    # Korttiostot
    def test_kun_kortilla_on_tarpeeksi_rahaa_saldo_pienenee(self):
        edullinen_onnistui = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        maukas_onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo_euroina(), 13.6)
        self.assertTrue(edullinen_onnistui and maukas_onnistui)

    def test_kun_kortilla_on_tarpeeksi_rahaa_myyntimaarakasvaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.edullisia_myyty(), 1)
        self.assertEqual(self.kassapaate.maukkaita_myyty(), 1)

    def test_kun_kortilla_ei_ole_tarpeeksi_rahaa_saldo_pysyy(self):
        kortti = Maksukortti(200)
        edullinen_onnistui = self.kassapaate.syo_edullisesti_kortilla(kortti)
        maukas_onnistui = self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(kortti.saldo_euroina(), 2)
        self.assertTrue(not edullinen_onnistui and not maukas_onnistui)

    def test_kun_kortilla_ei_ole_tarpeeksi_rahaa_myynti_ei_kasva(self):
        kortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(self.kassapaate.edullisia_myyty(), 0)
        self.assertEqual(self.kassapaate.maukkaita_myyty(), 0)

    def test_kortilla_ostettaessa_kassan_rahat_eivat_muutu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_kortin_saldon_lataus_toimii_odotetusti(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)

        self.assertEqual(self.kortti.saldo_euroina(), 25)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1005)

    def test_kortin_saldon_lataus_ei_toimi_negatiivisella_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -100)

        self.assertEqual(self.kortti.saldo_euroina(), 20)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
