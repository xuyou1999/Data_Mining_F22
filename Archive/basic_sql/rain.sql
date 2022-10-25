SELECT mode, is_rain, AVG(speed) as avg_speed, 
AVG(how_long_delay_or_ahead) AS avg_delay, variance(speed), Count(*)
FROM vehicle_time
where EXTRACT(hour FROM calendar_time)  >= 4 
and EXTRACT(hour FROM calendar_time) <= 21
Group by is_rain, mode
ORDER by mode

