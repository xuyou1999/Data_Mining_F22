with cal_time_minute AS
(SELECT *, EXTRACT(hour FROM calendar_time)*60+
EXTRACT(minutes FROM calendar_time)+
EXTRACT(seconds FROM calendar_time)/60  AS minite
from vehicle_time
WHERE EXTRACT(day FROM calendar_time) < 20)


-- specific stop and time section
(SELECT mode, FLOOR(minite/30) AS minite_30_times, 
t_cls, is_rain, is_weekend, stop_sequence,
-1 AS stop_section, 
line_id, variante,
AVG(speed) AS avg_speed,
AVG(how_long_delay_or_ahead) AS avg_delay,
Count(*)
FROM cal_time_minute 
Group by minite_30_times, mode, t_cls, is_rain, is_weekend, stop_sequence, line_id, variante
ORDER by mode)

UNION ALL

-- stop_section and time section
(SELECT mode, FLOOR(minite/30) AS minite_30_times, 
t_cls, is_rain, is_weekend, -1 AS stop_sequence,
FLOOR(stop_sequence/3.0) AS stop_section, 
line_id, variante,
AVG(speed) AS avg_speed,
AVG(how_long_delay_or_ahead) AS avg_delay,
Count(*)
FROM cal_time_minute 
Group by minite_30_times, mode, t_cls, is_rain, is_weekend, stop_section, line_id, variante
ORDER by mode)

UNION ALL


-- only specific stop
(SELECT mode, -1 AS minite_30_times, 
t_cls, is_rain, is_weekend, stop_sequence,
-1 AS stop_section, 
line_id, variante,
AVG(speed) AS avg_speed,
AVG(how_long_delay_or_ahead) AS avg_delay,
Count(*)
FROM cal_time_minute 
Group by mode, t_cls, is_rain, is_weekend, stop_sequence, line_id, variante
ORDER by mode)

UNION ALL

-- only stop_section 
(SELECT mode, -1 AS minite_30_times, 
t_cls, is_rain, is_weekend, -1 AS stop_sequence,
FLOOR(stop_sequence/3.0) AS stop_section, 
line_id, variante,
AVG(speed) AS avg_speed,
AVG(how_long_delay_or_ahead) AS avg_delay,
Count(*)
FROM cal_time_minute 
Group by mode, t_cls, is_rain, is_weekend, stop_section, line_id, variante
ORDER by mode)

UNION ALL

-- directed line and time section
(SELECT mode, FLOOR(minite/30) AS minite_30_times, 
t_cls, is_rain, is_weekend, -1 AS stop_sequence,
-1 AS stop_section, 
line_id, variante,
AVG(speed) AS avg_speed,
AVG(how_long_delay_or_ahead) AS avg_delay,
Count(*)
FROM cal_time_minute 
Group by minite_30_times, mode, t_cls, is_rain, is_weekend, line_id, variante
ORDER by mode)

UNION ALL

-- only time section
(SELECT mode, FLOOR(minite/30) AS minite_30_times, 
t_cls, is_rain, is_weekend, -1 AS stop_sequence,
-1 AS stop_section, 
-1 AS line_id, -1 AS variante,
AVG(speed) AS avg_speed,
AVG(how_long_delay_or_ahead) AS avg_delay,
Count(*)
FROM cal_time_minute 
Group by minite_30_times, mode, t_cls, is_rain, is_weekend
ORDER by mode)

UNION ALL

-- only trip section
(SELECT mode, -1 AS minite_30_times, 
t_cls, is_rain, is_weekend, -1 AS stop_sequence,
-1 AS stop_section, 
line_id, variante,
AVG(speed) AS avg_speed,
AVG(how_long_delay_or_ahead) AS avg_delay,
Count(*)
FROM cal_time_minute 
Group by mode, t_cls, is_rain, is_weekend, line_id, variante
ORDER by mode)

UNION ALL

-- the least info section: mode and environment
(SELECT mode, -1 AS minite_30_times, 
t_cls, is_rain, is_weekend, -1 AS stop_sequence,
-1 AS stop_section, 
-1 AS line_id, -1 AS variante,
AVG(speed) AS avg_speed,
AVG(how_long_delay_or_ahead) AS avg_delay,
Count(*)
FROM cal_time_minute 
Group by mode, t_cls, is_rain, is_weekend
ORDER by mode)




