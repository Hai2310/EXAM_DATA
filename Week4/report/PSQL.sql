CREATE TABLE op_per_year (
	year BIGINT , 
	avg_rating DOUBLE PRECISION ,
	total_votes BIGINT
)

CREATE TABLE op_rating (
	episode BIGINT ,
	name VARCHAR(255) ,
	trend VARCHAR(30) ,
	rating VARCHAR(30)
)

SELECT * FROM OP_PER_YEAR 
SELECT * FROM OP_RATING