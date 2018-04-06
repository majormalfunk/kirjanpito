## Tietokantakuvaus

Kuvaus on vielä kesken. Kuvauksesta puuttuu mm. tositteiden hyväksyntään tarvittavat taulut ja sarakkeet tauluista.
Lisäksi entity_id:llä on tässä toteutettu eri toimijoiden erottaminen toisistaan. Lopulliseen versioon tulee valita toteutustapa.
Etuna kaikkiin tauluihin laitettavalla entity_id:llä on se, että pystytään varmemmin ja nopeammin poimimaan vain käsiteltävän
toimijan kirjanpito. Toisaalta foreign key -viittaus jokaisessa taulussa voi hidastaa toimintaa. Onko näin?

### Tietokantakaavio:

![Tietokantakaavio](https://github.com/majormalfunk/kirjanpito/blob/master/documentation/Tietokantakaavio.png "Tietokantakaavio")
