## Tietokantakuvaus

Tietokantakuvaus on päivitetty.

Entity_id löytyy tässä joka taulusta, jotta kyselyt on helpompi toteuttaa ja koska siten on helpompi varmistaa, ettei eri toimijoinden tiedot mene keskenään sekaisin vaikka toimitaan yhdessä tietokannassa. Lisäksi etuna kaikkiin tauluihin laitettavalla entity_id:llä on se, että pystytään varmemmin ja nopeammin poimimaan vain käsiteltävän toimijan kirjanpito. Toisaalta foreign key -viittaus jokaisessa taulussa voi hidastaa toimintaa.

### Tietokantakaavio:

![Tietokantakaavio](https://github.com/majormalfunk/kirjanpito/blob/master/documentation/Tietokantakaavio.png "Tietokantakaavio")


### Taulujen luontilauseet:

'''
CREATE TABLE entity (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	code VARCHAR(9), 
	name VARCHAR(100), 
	description VARCHAR(255), 
	PRIMARY KEY (id)
);
CREATE TABLE account_group (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(255), 
	inuse BOOLEAN NOT NULL, 
	number INTEGER NOT NULL, 
	entity_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT accountgroup_entity_uc UNIQUE (number, entity_id), 
	CHECK (inuse IN (0, 1)), 
	FOREIGN KEY(entity_id) REFERENCES entity (id)
);
CREATE TABLE user_account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	username VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	entity_id INTEGER NOT NULL, 
	role VARCHAR(10), 
	PRIMARY KEY (id), 
	FOREIGN KEY(entity_id) REFERENCES entity (id)
);
CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(255), 
	inuse BOOLEAN NOT NULL, 
	number INTEGER NOT NULL, 
	accountgroup_id INTEGER NOT NULL, 
	entity_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT account_entity_uc UNIQUE (number, entity_id), 
	CHECK (inuse IN (0, 1)), 
	FOREIGN KEY(accountgroup_id) REFERENCES account_group (id), 
	FOREIGN KEY(entity_id) REFERENCES entity (id)
);
CREATE TABLE fiscal_year (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	closed BOOLEAN NOT NULL, 
	locked BOOLEAN NOT NULL, 
	startdate DATE NOT NULL, 
	enddate DATE NOT NULL, 
	name VARCHAR(4) NOT NULL, 
	entity_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fiscalyear_entity_uc UNIQUE (name, entity_id), 
	CHECK (closed IN (0, 1)), 
	CHECK (locked IN (0, 1)), 
	FOREIGN KEY(entity_id) REFERENCES entity (id)
);
CREATE TABLE fiscal_period (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	closed BOOLEAN NOT NULL, 
	locked BOOLEAN NOT NULL, 
	startdate DATE NOT NULL, 
	enddate DATE NOT NULL, 
	name VARCHAR(6) NOT NULL, 
	fiscalyear_id INTEGER NOT NULL, 
	entity_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fiscalperiod_entity_uc UNIQUE (name, entity_id), 
	CHECK (closed IN (0, 1)), 
	CHECK (locked IN (0, 1)), 
	FOREIGN KEY(fiscalyear_id) REFERENCES fiscal_year (id), 
	FOREIGN KEY(entity_id) REFERENCES entity (id)
);
CREATE TABLE document_type (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(255), 
	inuse BOOLEAN NOT NULL, 
	doctype VARCHAR NOT NULL, 
	entity_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT documenttype_entity_uc UNIQUE (doctype, entity_id), 
	CHECK (inuse IN (0, 1)), 
	FOREIGN KEY(entity_id) REFERENCES entity (id)
);
CREATE TABLE activity (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(255), 
	inuse BOOLEAN NOT NULL, 
	code INTEGER NOT NULL, 
	orderer INTEGER NOT NULL, 
	entity_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT activity_entity_uc UNIQUE (code, entity_id), 
	CHECK (inuse IN (0, 1)), 
	FOREIGN KEY(entity_id) REFERENCES entity (id)
);
CREATE TABLE domain (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(255), 
	inuse BOOLEAN NOT NULL, 
	code INTEGER NOT NULL, 
	orderer INTEGER NOT NULL, 
	entity_id INTEGER NOT NULL, 
	activity_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT domain_entity_uc UNIQUE (code, entity_id), 
	CHECK (inuse IN (0, 1)), 
	FOREIGN KEY(entity_id) REFERENCES entity (id), 
	FOREIGN KEY(activity_id) REFERENCES activity (id)
);
CREATE TABLE ledger_document (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	documenttype_id INTEGER NOT NULL, 
	documentnumber INTEGER NOT NULL, 
	ledgerdate DATE NOT NULL, 
	description VARCHAR(255) NOT NULL, 
	recorded_by VARCHAR(144) NOT NULL, 
	approved_by VARCHAR(144), 
	entity_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ledgerdoc_number_type_entity_uc UNIQUE (documentnumber, documenttype_id, entity_id), 
	FOREIGN KEY(documenttype_id) REFERENCES document_type (id), 
	FOREIGN KEY(entity_id) REFERENCES entity (id)
);
CREATE TABLE ledger_row (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	ledgerdocument_id INTEGER NOT NULL, 
	account_id INTEGER NOT NULL, 
	amount INTEGER NOT NULL, 
	domain_id INTEGER NOT NULL, 
	description VARCHAR(255) NOT NULL, 
	recorded_by VARCHAR(144) NOT NULL, 
	approved_by VARCHAR(144), 
	entity_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ledgerdocument_id) REFERENCES ledger_document (id), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(domain_id) REFERENCES domain (id), 
	FOREIGN KEY(entity_id) REFERENCES entity (id)
);
'''
