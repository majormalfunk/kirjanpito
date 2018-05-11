# Kirjanpito
Tietokantasovellus / Harjoitustyö

Harjoitustyön tavoitteena oli rakentaa perustoiminnallisuudet sisältävä kirjanpitosovellus käytettäväksi esimerkiksi pienessä yhdistyksessä, joka haluaa siirtyä käyttämään sähköistä järjestelmää perinteisen tilikirjan sijaan.

Tarkoituksena oli luoda järjestelmä, jonka toiminta perustuu kirjanpidon tapahtumien tallentamiseen pankin tiliotteelta tai kassatositteilta. Tavoitteena oli, että järjestelmästä olisi voinut tulostaa kirjanpidon perusraportit kuten päiväkirjan, pääkirjan, tuloslaskelman ja taseen sekä suppean version tilinpäätöksestä.

Järjestelmään ei ollut tarkoitus rakentaa myyntilaskutusta tai jäsenmaksulaskutusta eikä myöskään jäsenrekisteriä. Koska pienet yhdistykset ovat harvoin arvonlisäverovelvollisia, niin järjestelmässä ei ole myöskään alv-laskentaa.

Järjestelmään oli tarkoitus luoda seuraavat käyttäjäroolit:
- kirjanpitäjä/rahastonhoitaja, joka tekee kirjaukset ja laatii tilinpäätöksen sekä toimii admin-roolissa
- hallituksen edustaja, joka hyväksyy kirjaukset
- toiminnantarkastaja, joka voi tarkastella kirjanpitoa ja raportteja.

Perustoiminnallisuudet ehdin saada aikaiseksi. Järjestelmään voi luoda tilikartan (tiliryhmiä ja niihin tilejä), laskentakohteet (toimintoja ja niiden alle kustannuspaikkoja), tilikaudet (tilikausi ja sen alle kaudet), tositelajit ja siinä voi tallentaa, muokata ja poistaa kaikkia edellä mainittuja. Myös tositteita voi tallentaa, muokata ja poistaa sekä tositteella voi lisätä tositerivejä, joita voi myös muokata ja poistaa. Sovelluksessa on toimivina rooleina pääkäyttäjä (kirjanpitäjä, joka voi muokata asetuksia ja tehdä luoda uusia käyttäjiä) sekä hyväksyjä, joka voi hyväksyä kirjanpitäjän tekemiä tositteita. Kirjanpitäjä ei voi itse hyväksyä tositteita eikä toisaalta hyväksyjä voi muokata tositteita. Hyväksyttyä tositetta ei voi enää muuttaa.

En aikataulun rajoitteiden vuoksi päässyt edes aloittamaan raporttien tekemistä, joten kirjanpitojärjestelmänä sovellus on nykyisessä muodossaan aika hyödytön. En myöskään saanut desimaalilukujen käsittelyä toimimaan kurssin työvälineillä, joten kirjaa pitää pitää vain kokonaisluvuilla. Mutta sehän on olennaisuuden periaatteen mukaista muutenkin.

Valitsemani aihe oli varmaankin turhan laaja näin lyhyessä ajassa toteutettavaksi varsinkin, kun työvälineistä oli iso osa ennestään tuntemattomia minulle. Voi olla, että tutummilla välineillä olisin päässyt paljon pitemmälle. Tällä kokoonpanolla kulutin hyvin paljon aikaa hyvinkin pienien toimintojen aikaansaamiseksi. Osittain ongelmia tuli uuden ohjelmointikielen syntaksin kanssa mutta ehkä enemmän päänvaivaa aiheutti kaikki muut minulle uudet välineet (wtforms, jinja, sqlalchemy jne). Niiden kanssa saatoi hukata tuntikausia ihmetellen minkä takia en saa tietorakenteessa olevaa tietoa käyttööni vaikka se siellä selvästi olikin.

Ajantasaiset käyttötapaukset ja tietokantakuvaus löytyy alla olevien linkkien takaa. Itse sovelluksessa on muutama neuvo käyttöönottoon.

[Käyttötapaukset](https://github.com/majormalfunk/kirjanpito/blob/master/documentation/kayttotapaukset)

[Tietokantakuvaus](https://github.com/majormalfunk/kirjanpito/blob/master/documentation/Tietokantakuvaus.md)

Sovellus on asennettuna Herokuun:

[Sovellus Herokussa](https://kirjanpython.herokuapp.com)
