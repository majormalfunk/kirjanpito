## Tietokantakuvaus

Tietokantakuvaus on päivitetty.

Entity_id löytyy tässä joka taulusta, jotta kyselyt on helpompi toteuttaa ja koska siten on helpompi varmistaa, ettei eri toimijoinden tiedot mene keskenään sekaisin vaikka toimitaan yhdessä tietokannassa. Lisäksi etuna kaikkiin tauluihin laitettavalla entity_id:llä on se, että pystytään varmemmin ja nopeammin poimimaan vain käsiteltävän toimijan kirjanpito. Toisaalta foreign key -viittaus jokaisessa taulussa voi hidastaa toimintaa.

### Tietokantakaavio:

![Tietokantakaavio](https://github.com/majormalfunk/kirjanpito/blob/master/documentation/Tietokantakaavio.png "Tietokantakaavio")
