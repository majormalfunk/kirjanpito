# kirjanpito
Tietokantasovellus / Harjoitustyö

Tämä on perustoiminnalisuudet sisältävä kirjanpitosovellus käytettäväksi esimerkiksi pienessä yhdistyksessä, joka haluaa siirtyä käyttämään sähköistä järjestelmää.
Järjestelmän toiminta perustuu kirjanpidon tapahtumien tallentamiseen pankin tiliotteelta tai kassatositteilta.
Järjestelmästä voi tulostaa kirjanpidon perusraportit kuten päiväkirjan, pääkirjan, tuloslaskelman ja taseen sekä suppean version tilinpäätöksestä.
Järjestelmässä ei ole myyntilaskusta tai jäsenmaksulaskutusta eikä jäsenrekisteriä. Koska pienet yhdistykset ovat harvoin arvonlisäverovelvollisia, niin järjestelmässä ei ole myöskään alv-laskentaa.

Järjestelmässä on seuraavat käyttäjäroolit:
- kirjanpitäjä/rahastonhoitaja, joka tekee kirjaukset ja laatii tilinpäätöksen
- hallituksen edustaja, joka hyväksyy kirjaukset
- toiminnantarkastaja, joka tarkastaa kirjanpidon ja tilinpäätöksen.

Käyttötapauksista ja tietokantakuvauksesta puuttuu tositteiden hyväksyntä ja tarkastaminen.

[Tietokantakaavio](https://github.com/majormalfunk/kirjanpito/blob/master/documentation/Tietokantakaavio.png)

[Sovellus Herokussa](https://kirjanpython.herokuapp.com)
