class Kassapaate:
    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0

    def kateismaksu(self, maksu, hinta, edullinen):
        if maksu >= hinta:
            self.kassassa_rahaa = self.kassassa_rahaa + hinta
            if edullinen:
                self.edulliset += 1
            else:
                self.maukkaat += 1
            return maksu - hinta
        else:
            return maksu

    def syo_edullisesti_kateisella(self, maksu):
        return self.kateismaksu(maksu, 240, True)

    def syo_maukkaasti_kateisella(self, maksu):
        return self.kateismaksu(maksu, 400, False)

    def korttimaksu(self, kortti, hinta, edullinen):
        if kortti.saldo >= hinta:
            kortti.ota_rahaa(hinta)
            if edullinen:
                self.edulliset += 1
            else:
                self.maukkaat += 1
            return True
        else:
            return False

    def syo_edullisesti_kortilla(self, kortti):
        return self.korttimaksu(kortti, 240, True)

    def syo_maukkaasti_kortilla(self, kortti):
        return self.korttimaksu(kortti, 400, False)

    def lataa_rahaa_kortille(self, kortti, summa):
        if summa >= 0:
            kortti.lataa_rahaa(summa)
            self.kassassa_rahaa += summa
        else:
            return

    def kassassa_rahaa_euroina(self):
        return self.kassassa_rahaa / 100

    def maukkaita_myyty(self):
        return self.maukkaat

    def edullisia_myyty(self):
        return self.edulliset
