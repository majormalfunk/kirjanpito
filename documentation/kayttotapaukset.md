Käyttötapaukset

1) Lähtötietojen perustaminen

Käyttöönoton aluksi tallennetaan lähtötiedot:
- kirjanpidon tiliryhmät (account group)
- kirjanpidon tilit (account)
- tositelajit (document type)
- aktiviteetit (activity)
- kustannuspaikat (domain)

Näissä toteutus on sqlalchemyllä.

2) Uuden tilikauden perustaminen

Perustietojen ollessa kunnossa perustetaan tilikausi:
- tilikausi (fiscal year)
- tilikauden jaksot eli käytännössä kuukaudet (fiscal period)

Tilikauden perustaminen luo myös jaksot.

3) Tositteiden tallentaminen

Tositteet tallennetaan esim pankkitiliotteen perusteella.
Tositteelle kirjataan:
- tositelaji (document type)
- kirjauspäivä -> kausi (fiscal period)
- selite

Tositteen riveille kirjataan:
- kirjanpidon tili (account)
- summa (debet = +, kredit = -)
- selite
- kustannuspaikka (domain)
- aktiviteetti (activity)

4) Raporttien tulostaminen

Sovelluksesta voidaan tulostaa
- määriteltyjä raportteja kuten tuloslaskelma ja tase
- tapahtumaluettelomuotoisia raportteja kuten päiväkirja ja pääkirja

5) Kausien sulkeminen

Kun kauden tai tilikauden kirjanpito on valmis, kausi voidaan sulkea
