
-- Table: users
CREATE TABLE users ( 
    user_id   INTEGER         PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR( 80 )   NOT NULL
                              UNIQUE
                              COLLATE 'NOCASE',
    user_acct VARCHAR( 80 )   NOT NULL
                              UNIQUE
                              COLLATE 'NOCASE',
    user_salt CHAR( 8 )       NOT NULL,
    user_pswd CHAR( 32 )      NOT NULL,
    user_perm INT( 10 )       NOT NULL
                              DEFAULT ( 0 ),
    user_logo VARCHAR( 500 ),
    user_mail VARCHAR( 500 ),
    user_sign VARCHAR( 500 ),
    user_ctms INT( 10 )       NOT NULL,
    user_utms INT( 10 ),
    user_atms INT( 10 ) 
);


-- Index: idx_userAcct
CREATE UNIQUE INDEX idx_userAcct ON users ( 
    user_acct
);

CREATE UNIQUE INDEX idx_userName ON users ( 
    user_name
);

INSERT INTO [users] ([user_id], [user_name], [user_acct], [user_salt], [user_pswd], [user_perm], [user_logo], [user_mail], [user_sign], [user_ctms], [user_utms], [user_atms]) VALUES (1, 'Admin', 'admin', 'asdflkjh', 'b6ce17f5578131e2997ccfb99dcc3500', 2147483647, '', 'admin@luokr.com', '', 1374486661, 1374786660, 1374765138);
