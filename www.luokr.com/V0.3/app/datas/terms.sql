
-- Table: terms
CREATE TABLE terms ( 
    term_id   INTEGER        PRIMARY KEY AUTOINCREMENT,
    term_name VARCHAR( 30 )  NOT NULL,
    term_sign VARCHAR( 30 )  NOT NULL
                             UNIQUE,
    term_refc INT( 10 )      DEFAULT ( 0 ),
    term_ctms INT( 10 ) 
);
