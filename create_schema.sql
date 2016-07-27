USE toastmasters;

DROP TABLE IF EXISTS members;
CREATE TABLE members ( id    INTEGER AUTO_INCREMENT PRIMARY KEY,
                       fname VARCHAR(32) NOT NULL,
                       lname VARCHAR(32) NOT NULL,
                       title VARCHAR(8)  NOT NULL DEFAULT "TM" ); 

DROP TABLE IF EXISTS known_meetings;
CREATE TABLE known_meetings ( dayof       DATE PRIMARY KEY,
                              toastmaster INTEGER REFERENCES members,
                              topicmaster INTEGER REFERENCES members,
                              geneval     INTEGER REFERENCES members,
                              grammarian  INTEGER REFERENCES members,
                              votecounter INTEGER REFERENCES members,
                              ahcounter   INTEGER REFERENCES members,
                              jokemaster  INTEGER REFERENCES members,
                              listener    INTEGER REFERENCES members,
                              momenttm    INTEGER REFERENCES members,
                              speaker1    INTEGER REFERENCES members,
                              speaker2    INTEGER REFERENCES members,
                              speaker3    INTEGER REFERENCES members,
                              eval1       INTEGER REFERENCES members,
                              eval2       INTEGER REFERENCES members,
                              eval3       INTEGER REFERENCES members,
                              timer       INTEGER REFERENCES members );

DROP TABLE IF EXISTS role_history;  
CREATE TABLE role_history ( who         INTEGER PRIMARY KEY REFERENCES members,
                            toastmaster INTEGER NOT NULL DEFAULT 0,
                            topicmaster INTEGER NOT NULL DEFAULT 0,
                            geneval     INTEGER NOT NULL DEFAULT 0,
                            speaker     INTEGER NOT NULL DEFAULT 0,
                            eval        INTEGER NOT NULL DEFAULT 0,
                            timer       INTEGER NOT NULL DEFAULT 0,
                            grammarian  INTEGER NOT NULL DEFAULT 0,
                            ahcounter   INTEGER NOT NULL DEFAULT 0,
                            momenttm    INTEGER NOT NULL DEFAULT 0,
                            jokemaster  INTEGER NOT NULL DEFAULT 0,
                            listener    INTEGER NOT NULL DEFAULT 0,
                            votecounter INTEGER NOT NULL DEFAULT 0 );


DROP TABLE IF EXISTS to_be_absent;
CREATE TABLE to_be_absent ( event INTEGER AUTO_INCREMENT PRIMARY KEY,
                            who   INTEGER NOT NULL REFERENCES members,
                            dayof DATE NOT NULL);
