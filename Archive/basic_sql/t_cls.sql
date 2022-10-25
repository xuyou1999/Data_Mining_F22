SELECT mode, t_cls, AVG(speed), AVG(how_long_delay_or_ahead) AS avg_delay, 
variance(speed), Count(*)
FROM vehicle_time
where EXTRACT(hour FROM calendar_time)  >= 4 
and EXTRACT(hour FROM calendar_time) <= 21
Group by t_cls, mode

ORDER by mode
