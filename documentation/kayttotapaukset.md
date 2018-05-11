Käyttötapaukset

1) Lähtötietojen perustaminen

Käyttöönoton aluksi tallennetaan lähtötiedot:
- kirjanpidon tiliryhmät (account group)
- kirjanpidon tilit (account)
- tositelajit (document type)
- aktiviteetit (activity)
- kustannuspaikat (domain)

Näissä toteutus on sqlalchemyllä ja käsin kirjoitetuilla sql -lauseilla.
Kaikki tiliryhmät ja tili haetaan kyselyllä:

```
            SELECT
            ag.id, ag.number, ag.name, ag.description, ag.inuse,
            a.id, a.number, a.name, a.description, a.inuse
            FROM account_group ag
            LEFT JOIN account a on ag.id = a.accountgroup_id
            WHERE ag.entity_id = :entity_id
            ORDER BY ag.number, a.number
```

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

Tositteet haetaan listausnäkymään seuraavalla kyselyllä:

```
            SELECT
            ld.id, ld.documenttype_id, dt.doctype, ld.documentnumber,
            ld.ledgerdate, fy.name, fp.name,
            ld.description, ld.recorded_by, ld.approved_by, ld.entity_id,
            SUM(lr.amount) AS amount
            FROM ledger_document ld
            LEFT JOIN ledger_row lr on lr.ledgerdocument_id = ld.id,
            document_type dt, fiscal_year fy, fiscal_period fp
            WHERE dt.id = ld.documenttype_id
            AND ld.ledgerdate >= fp.startdate AND ld.ledgerdate <= fp.enddate
            AND fy.id = fp.fiscalyear_id
            AND ld.entity_id = :entity_id
            AND dt.entity_id = ld.entity_id
            AND fy.entity_id = ld.entity_id
            AND fp.entity_id = ld.entity_id 
            AND (fy.id = :fiscalyear_id OR :fiscalyear_id is null)
            AND (fp.id = :fiscalperiod_id OR :fiscalperiod_id is null)
            GROUP BY " +
            ld.id, ld.documenttype_id, dt.doctype, ld.documentnumber,
            ld.ledgerdate, fy.name, fp.name,
            ld.description, ld.recorded_by, ld.approved_by, ld.entity_id
            ORDER BY ld.ledgerdate DESC, dt.doctype ASC, ld.documentnumber ASC
```

Valitettavasti en ehtinyt toteuttamaan hakua kausi ja jakso haulla.

4) Raporttien tulostaminen

Raportteja en ehtinyt toteuttamaan

5) Kausien sulkeminen

Kun kauden tai tilikauden kirjanpito on valmis, kausi voidaan sulkea. Valitettavasti en myöskään ehtinyt toteuttamaan sitä että kauden sulkemisella olisi mitään vaikutusta.

