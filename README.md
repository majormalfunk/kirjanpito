# kirjanpito
Tietokantasovellus / Harjoitustyö

Tämä on perustoiminnalisuudet sisältävä kirjanpitosovellus käytettäväksi esimerkiksi pienessä yhdistyksessä, joka haluaa siirtyä käyttämään sähköistä järjestelmää.
Järjestelmän toiminta perustuu kirjanpidon tapahtumien tallentamiseen pankin tiliotteelta tai kassatositteilta.
Järjestelmästä voi tulostaa kirjanpidon perusraportit kuten päiväkirjan, pääkirjan, tuloslaskelman ja taseen sekä suppean version tilinpäätöksestä.
Järjestelmässä ei ole myyntilaskusta tai jäsenmaksulaskutusta eikä jäsenrekisteriä. Koska pienet yhdistykset ovat harvoin arvonlisäverovelvollisia, niin järjestelmässä ei ole myöskään alv-laskentaa.

Järjestelmässä on seuraavat käyttäjäroolit:
- kirjanpitäjä/rahastonhoitaja, joka tekee kirjaukset ja laatii tilinpäätöksen sekä toimii admin-roolissa
- hallituksen edustaja, joka hyväksyy kirjaukset
- toiminnantarkastaja, joka voi tarkastella kirjanpitoa ja raportteja.

Käyttötapauksista ja tietokantakuvauksesta puuttuu tositteiden hyväksyntä ja tarkastaminen.

[Käyttötapaukset](https://github.com/majormalfunk/kirjanpito/blob/master/documentation/kayttotapaukset)
[Tietokantakuvaus](https://github.com/majormalfunk/kirjanpito/blob/master/documentation/Tietokantakuvaus.md)

[Sovellus Herokussa](https://kirjanpython.herokuapp.com)
