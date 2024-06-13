-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computeS and store the average weighted score for a studenT
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
  user_id INT
)
BEGIN
    DECLARE weighted_score FLOAT;
    DECLARE weights FLOAT;

    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO weighted_score, weights
    FROM corrections c
    INNER JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;


    UPDATE users
    SET average_score = IF(weights = 0, 0, weighted_score / weights)
    WHERE users.id = user_id;
END //
DELIMITER ;