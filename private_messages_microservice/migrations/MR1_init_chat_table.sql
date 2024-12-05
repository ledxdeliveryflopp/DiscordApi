-- +migrate Up
-- SQL in section 'Up' is executed when this migration is applied
CREATE TABLE users (id SERIAL PRIMARY KEY, username varchar);

CREATE TABLE private_chat (id serial PRIMARY KEY, chat_starter_id integer, chat_recipient_id integer,
                           FOREIGN KEY (chat_starter_id) REFERENCES users(id), FOREIGN KEY (chat_recipient_id) REFERENCES users(id));

CREATE TABLE message (id SERIAL PRIMARY KEY, text varchar, owner_id integer, chat_id integer,
                      FOREIGN KEY (owner_id) REFERENCES users(id), FOREIGN KEY (chat_id) REFERENCES private_chat(id));



-- +migrate Down
-- SQL section 'Down' is executed when this migration is rolled back
DROP TABLE users;
DROP TABLE private_chat;
DROP TABLE message;