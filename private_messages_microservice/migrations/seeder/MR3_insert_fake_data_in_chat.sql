-- +migrate Up
-- SQL in section 'Up' is executed when this migration is applied
INSERT INTO private_chat (chat_starter_id, chat_recipient_id)
VALUES (1, 2), (2, 1);

-- +migrate Down
-- SQL section 'Down' is executed when this migration is rolled back
DELETE FROM private_chat WHERE id = 1;