-- SQL script to create an index idx_name_first on the first
-- letter of name in the names table and score

CREATE INDEX idx_name_first_score
ON names(name(1), score);