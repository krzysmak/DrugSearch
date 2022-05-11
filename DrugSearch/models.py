from django.db import models

class SzczegolyRefundacji(models.Model):
    #id = models.TextField(primary_key=True)
    identyfikator_leku = models.TextField(blank=True, null=True)
    zakres_wskazan = models.TextField(blank=True, null=True)
    zakres_wskazan_pozarejestracyjnych = models.TextField(blank=True, null=True)
    poziom_odplatnosci = models.TextField(blank=True, null=True)
    wysokosc_doplaty = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    # lek = models.ForeignKey('Lek', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.identyfikator_leku + " " + self.zakres_wskazan

class Lek(models.Model):
    #id = models.TextField(primary_key=True)
    nazwa_leku = models.TextField()
    substancja_czynna = models.TextField()
    postac = models.TextField()
    dawka_leku = models.TextField()
    zawartosc_opakowania = models.TextField()
    identyfikator_leku = models.TextField()
    refundacje = models.ManyToManyField(SzczegolyRefundacji)

    def __str__(self):
        return self.nazwa_leku + "" + self.identyfikator_leku
