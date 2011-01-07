DROP TABLE IF EXISTS decos;
DROP TABLE IF EXISTS aterros;
DROP TABLE IF EXISTS ailes;
DROP TABLE IF EXISTS vols;

-- could have pointers between decos and aterros
CREATE TABLE decos (iname VARCHAR(50) PRIMARY KEY, infos VARCHAR(100));
CREATE TABLE aterros (iname VARCHAR(50) PRIMARY KEY, infos VARCHAR(100));

CREATE TABLE ailes (iname VARCHAR(50) PRIMARY KEY, infos VARCHAR(100));


CREATE TABLE vols (
       id INTEGER PRIMARY KEY AUTOINCREMENT, 
       story VARCHAR(5000),
       ddate DATETIME, 	  
       duration TIME,
       dist INTEGER, 
       altmax INTEGER, 
       maxgain INTEGER, 
       gaintotal INTEGER, 
       lowestpt INTEGER,
       aile VARCHAR(50),
       deco VARCHAR(50),
       aterro VARCHAR(50),
       vtype VARCHAR(20)
);



-- insert dumb values

-- INSERT INTO decos VALUES ('saint hilaire nord', 'moquette');
INSERT INTO decos VALUES ('Saint Hilaire - Déco Nord', '');
-- INSERT INTO decos VALUES ('saleve table', 'moquette');

INSERT INTO aterros VALUES ('Lumbin', '');
-- INSERT INTO aterros VALUES ('pont de zone', 'tout moche');

INSERT INTO ailes VALUES ('X-ray', 'violette, vieille');
INSERT INTO ailes VALUES ('AspenII', 'Red/Gold');

-- INSERT INTO vols VALUES (null, 
--        'vide',
--        '2007-02-25 12:05:00', 
--        '00:20:00',
--        '20', 
--        '2200', 
--        '1000', 
--        '1500', 
--        '1200', 
--        'x-ray', 
--        'saint hilaire nord', 
--        'lumbin'
-- );

-- INSERT INTO vols VALUES (null, 
--        'vide',
--        '2007-02-20 12:00:00', 
--        '0:26:00',
--        '45', 
--        '2100', 
--        '200', 
--        '400', 
--        '200', 
--        'x-ray', 
--        'saint hilaire sud', 
--        'lumbin'
-- );

-- INSERT INTO vols VALUES (null, 
--        'vide',
--        '2007-04-11 15:30:00', 
--        '1:45:00',
--        '45', 
--        '2100', 
--        '200', 
--        '400', 
--        '200', 
--        'x-ray', 
--        'saint hilaire sud', 
--        'lumbin'
-- );


-- INSERT INTO vols VALUES (null, 
--        'vide',
--        '2007-04-12 15:00:00', 
--        '2:30:00',
--        '45', 
--        '2100', 
--        '200', 
--        '400', 
--        '200', 
--        'x-ray', 
--        'saint hilaire sud', 
--        'lumbin'
-- );


-- INSERT INTO vols VALUES (null, 
--        'vide',
--        '2007-03-11 15:00:00', 
--        '0:55:00',
--        '45', 
--        '2100', 
--        '200', 
--        '400', 
--        '200', 
--        'x-ray', 
--        'saint hilaire sud', 
--        'lumbin'
-- );