# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 11:04:35 2022
"""
import re
import numpy as np
def datetime_calculator(Date1,Date2):
    
    #"H:M:S - H:M:S"
    pattern1 = r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
    if re.match(pattern1, Date1) is not None and re.match(pattern1, Date2) is not None:
        d1_seconds = int(Date1[0:2]) * 3600 + int(Date1[3:5]) * 60 + int(Date1[6:8])
        d2_seconds = int(Date2[0:2]) * 3600 + int(Date2[3:5]) * 60 + int(Date2[6:8])
        interval = d1_seconds - d2_seconds
        sign = np.sign(interval)
        
        hour = str(abs(interval) //3600)
        minutes = str(abs(interval) %3600 // 60)
        seconds = str(abs(interval) - abs(int(hour)) * 3600 - abs(int(minutes)) * 60)
        
        
        if re.match(r"^[0-9]$",hour) is not None:
            hour = "0"+hour
        
        if sign == -1:
            hour = "-"+hour
            
        if re.match(r"^[0-9]$",minutes) is not None:
            minutes = "0"+minutes
        if re.match(r"^[0-9]$",seconds) is not None:
            seconds = "0"+seconds
            
            
        return hour + ":" + minutes + ":" + seconds
    
        