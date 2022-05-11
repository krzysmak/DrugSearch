import decimal

from DrugSearch.models import Lek, SzczegolyRefundacji
import csv

from DrugSearch.serializers import LekSerializer


def run():
    # Lek.objects.all().delete()
    # SzczegolyRefundacji.objects.all().delete()
    #
    # # wczytywanie refundacji
    # with open('/Users/kacperjablonski/PycharmProjects/IO/WyszukiwarkaLekow/scripts/szczegoly.csv',
    #           errors='ignore') as file:
    #     reader = csv.reader(file)
    #     next(reader)  # Advance past the header
    #
    #     SzczegolyRefundacji.objects.all().delete()
    #
    #     for row in reader:
    #         print(row)
    #         # genre, _ = Genre.objects.get_or_create(name=row[-1])
    #         s = row[4]
    #         # lek_dodaj = Lek.objects.get(identyfikator_leku=row[0])
    #         doplata = 0
    #         if s:
    #             doplata = decimal.Decimal(s)
    #         refundacja = SzczegolyRefundacji(
    #             identyfikator_leku=row[0],
    #             zakres_wskazan=row[1],
    #             zakres_wskazan_pozarejestracyjnych=row[2],
    #             poziom_odplatnosci=row[3],
    #             wysokosc_doplaty=doplata,
    #             id=row[5],
    #         )
    #         refundacja.save()
    #
    # with open('/Users/kacperjablonski/PycharmProjects/IO/WyszukiwarkaLekow/scripts/leki.csv', errors='ignore') as file:
    #     reader = csv.reader(file)
    #     next(reader)  # Advance past the header
    #
    #     Lek.objects.all().delete()
    #
    #     for row in reader:
    #         print(row)
    #
    #         # genre, _ = Genre.objects.get_or_create(name=row[-1])
    #         lek = Lek(
    #             nazwa_leku=row[0],
    #             substancja_czynna=row[1],
    #             postac=row[2],
    #             dawka_leku=row[3],
    #             zawartosc_opakowania=row[4],
    #             identyfikator_leku=row[5],
    #             id=row[6]
    #         )
    #         lek.save()

    leki = Lek.objects.all()

    # for lek in leki:
    #     print(lek)
    #     refunds = SzczegolyRefundacji.objects.filter(identyfikator_leku=lek.identyfikator_leku)
    #     for refun in refunds:
    #         print(refun)
    #         lek.refundacje.add(refun)

    for lek in leki:
        lek_serialized = LekSerializer(lek)
        print(lek_serialized.data)
        # refund = lek.refundacje.all()
        # for ref in refund:
        #     print(ref)






