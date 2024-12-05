-- +migrate Up
-- SQL in section 'Up' is executed when this migration is applied
INSERT INTO users (username)

SELECT
    'User ' || generate_series(1, 1000) AS username;


-- +migrate Down
-- SQL section 'Down' is executed when this migration is rolled back
DELETE FROM users WHERE id = 1 and id = 2;