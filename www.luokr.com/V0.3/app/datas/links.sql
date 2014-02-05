
-- Table: links
CREATE TABLE links ( 
    link_id   INTEGER        PRIMARY KEY AUTOINCREMENT,
    link_name VARCHAR( 80 ),
    link_href TEXT,
    link_desp TEXT,
    link_rank INT( 10 )      DEFAULT ( 99 ),
    link_ctms INT( 10 ),
    link_utms INT( 10 ) 
);


-- Index: idx_linkRank
CREATE INDEX idx_linkRank ON links ( 
    link_rank 
);

