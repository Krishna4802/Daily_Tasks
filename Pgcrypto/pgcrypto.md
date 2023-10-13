    CREATE EXTENSION pgcrypto;

### Create table with Encryption

    CREATE TABLE pgcrypto (id serial PRIMARY KEY,  name text, dob date,  encrypted_data bytea );

##### Bytes -enables the storage of arbitrary raw binary strings regardless of database character encoding

### Inserting :

    INSERT INTO pgcrypto (name, dob, encrypted_data)
    VALUES (‘Krish’, ‘2002-08-04’, pgp_sym_encrypt(‘Krish’@123, 'MySecretKey'));

    INSERT INTO pgcrypto (name, dob, encrypted_data)
    VALUES (‘Ambuj’, ‘2002-10-15’, pgp_sym_encrypt(‘Ambuj’, 'MySecretKey'));

    INSERT INTO pgcrypto (name, dob, encrypted_data)
    VALUES (‘Anisha’, ‘2002-10-23’, pgp_sym_encrypt(‘Anisha@123’, 'MySecretKey'));
    
    INSERT INTO pgcrypto (name, dob, encrypted_data)
    VALUES (‘Shanthini’, ‘2001-09-22’, pgp_sym_encrypt(’S’halu@123, 'MySecretKey'));


### Select Query :

    SELECT id, name, dob, pgp_sym_decrypt(encrypted_data, 'MySecretKey') AS decrypted_data FROM pgcrypto;
    
    SELECT * from pgcrypto;

### To select That encrypted id :

    SELECT * FROM pgcrypto WHERE pgp_sym_decrypt(encrypted_data, 'MySecretKey') LIKE '%uj';

### Creating index

    CREATE INDEX idx_decrypted_data ON pgcrypto (pgp_sym_decrypt(encrypted_data, 'MySecretKey'));
    
    CREATE INDEX idx_encrypted_at ON pgcrypto (encrypted_data);

### Updating with encrypted_data column

    UPDATE pgcrypto
    SET name = 'Krishna'
    WHERE pgp_sym_decrypt(encrypted_data, 'MySecretKey') = 'Krish@123';
