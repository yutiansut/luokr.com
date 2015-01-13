
-- Table: users
CREATE TABLE users ( 
    user_id   INTEGER         PRIMARY KEY AUTOINCREMENT,
    user_auid VARCHAR( 64 )   NOT NULL
                              DEFAULT ( '' ),
    user_name VARCHAR( 64 )   NOT NULL
                              UNIQUE
                              COLLATE 'NOCASE',
    user_salt CHAR( 8 )       NOT NULL,
    user_pswd CHAR( 32 )      NOT NULL,
    user_perm INT( 10 )       NOT NULL
                              DEFAULT ( 0 ),
    user_mail VARCHAR( 64 )   NOT NULL
                              COLLATE 'NOCASE',
    user_sign VARCHAR( 128 )  NOT NULL
                              DEFAULT ( '' ),
    user_logo VARCHAR( 256 )  NOT NULL
                              DEFAULT ( '' ),
    user_ctms INT( 10 )       NOT NULL,
    user_utms INT( 10 )       NOT NULL,
    user_atms INT( 10 )       NOT NULL 
);

INSERT INTO [users] ([user_id], [user_name], [user_salt], [user_pswd], [user_perm], [user_mail], [user_sign], [user_logo], [user_ctms], [user_utms], [user_atms]) VALUES (1, 'admin', 'asdflkjh', 'b6ce17f5578131e2997ccfb99dcc3500', 2147483647, '', '', '', 1374486661, 1374786660, 1374765138);
