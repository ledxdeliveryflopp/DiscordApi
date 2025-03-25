-- +migrate Up
-- SQL in section 'Up' is executed when this migration is applied
INSERT INTO message (text, owner_id, chat_id)

SELECT
    'Test ' || generate_series(1, 1000) AS text,
    generate_series(1, 1000) AS owner_id,
    '1' AS chat_id;



-- +migrate Down
-- SQL section 'Down' is executed when this migration is rolled back
DELETE FROM message WHERE chat_id = 1;