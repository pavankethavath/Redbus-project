CREATE DATABASE redbus_data;

use redbus_data;

CREATE TABLE bus_routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name TEXT,
    route_link TEXT,
    busname TEXT,
    bustype TEXT,
    departing_time TIME,
    duration TEXT,
    reaching_time TIME,
    star_rating FLOAT,
    price DECIMAL(10, 2),
    seats_available INT
);

SELECT * FROM redbus_data.bus_routes;


# Checking the data types of the columns in the table
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'bus_routes' ;

# Counting duplicate data from the table 
SELECT route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available, COUNT(*)
FROM bus_routes
GROUP BY route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available
HAVING COUNT(*) > 1;


SET GLOBAL net_read_timeout=600;
SET GLOBAL net_write_timeout=600;
SET GLOBAL wait_timeout=600;
SET GLOBAL interactive_timeout=600;


# Removing duplicate rows
DELETE FROM bus_routes 
WHERE id IN (
    SELECT id FROM (
        SELECT t1.id
        FROM bus_routes t1
        INNER JOIN bus_routes t2 
        WHERE 
            t1.id > t2.id
            AND t1.route_name = t2.route_name
            AND t1.route_link = t2.route_link
            AND t1.busname = t2.busname
            AND t1.bustype = t2.bustype
            AND t1.departing_time = t2.departing_time
            AND t1.duration = t2.duration
            AND t1.reaching_time = t2.reaching_time
            AND t1.star_rating = t2.star_rating
            AND t1.price = t2.price
            AND t1.seats_available = t2.seats_available
        LIMIT 100
    ) AS temp
);



SELECT DISTINCT bustype
FROM bus_routes;

