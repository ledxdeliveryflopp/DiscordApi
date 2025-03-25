-- +migrate Up
-- SQL in section 'Up' is executed when this migration is applied
-- CREATE TABLE users (id SERIAL PRIMARY KEY, username varchar);

CREATE TABLE message (id SERIAL PRIMARY KEY, text varchar, answer integer, owner_id integer, chat_id integer,
                      FOREIGN KEY (owner_id) REFERENCES "users"(id),
                      FOREIGN KEY (answer) REFERENCES message(id) ON DELETE SET NULL,
                      FOREIGN KEY (chat_id) REFERENCES private_chat(id) ON DELETE CASCADE);

-- +migrate Down
-- SQL section 'Down' is executed when this migration is rolled back
DROP TABLE message;