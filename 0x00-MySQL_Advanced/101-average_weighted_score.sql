-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForAllUsers
-- that computes and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE weighted_score FLOAT;
    DECLARE weights FLOAT;
    DECLARE user_id INT;
    DECLARE user_id_not_present INT DEFAULT FALSE;

    -- cursor for iteration
    DECLARE cur CURSOR FOR
        SELECT id
        FROM users;

    -- Error Hnadling
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET user_id_not_present = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id;
        IF user_id_not_present THEN
            LEAVE read_loop;
        END IF;

        -- Calculate the weighted score and total weights for the current user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO weighted_score, weights
        FROM corrections c
        INNER JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;


        UPDATE users
        SET average_score = IF(weights = 0, 0, weighted_score / weights)
        WHERE users.id = user_id;
    END LOOP;

    CLOSE cur;
END //
DELIMITER ;