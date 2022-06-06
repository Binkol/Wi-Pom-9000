from termostat import Termostat
from bath import Bath
import matplotlib.pyplot as plt
import numpy as np
import time
from bokeh.plotting import figure, show
from progress.bar import Bar

#TODO zmniejszyć okres próbkowania #mamy
#TODO napisac funkcje w Termostacie, która przyjmuje sygnał sterujący jako parametr do sterowania procentem hot/cold
#TODO dopasować wartość sygnalu steorwania do wartości przyjmowanej przez termostat czyli od 0.0 do 1.0


temp_0 = 20 #water temperature at start
temp_target = 35

Tp = 0.1 #okres próbkowania 
t_sim = 1.5 * 3600
N = int(t_sim/Tp) 

kp = 0.15 #wzmocnienie regulatora
Ti = 7.5 #czas zdwojenia
Td = 0.2

termo = Termostat(60, 10, 5, 0.6) #(hot, cold, flow_spped, hot_percentage)
bath = Bath(temp_0, 10, 400)       #(start_water_temp, start_water_amount, smax_water_amount)
counter = 0

u_min = 0
u_max = 10
u_PID = [0.5, ]
bath_temps = []
alpha = [0.5, ]
e = [0.0, ]

def temp_pid():
    global u_PID
    bar = Bar('Processing', max=N-1)
    for i in range(N - 1):
        e.append(temp_target - bath.current_water_temp)
        u_PID.append(kp * (e[i] + Tp * sum(e) / Ti + Td * (e[i] - e[i-1]) / Tp))
        
        if u_PID[-1] < 10 and u_PID[-1] >= 0:
            termo.change_hot_percentage(u_PID[-1]/u_max)
        elif u_PID[-1] > 10:
            termo.change_hot_percentage(1.0)
        else:
            termo.change_hot_percentage(u_min)

        termo.update_water_temp()
        bath.mix_waters(Tp, termo.flow_speed, termo.mixed_water_temp)
        bath.update_water_amount(Tp, termo.flow_speed)

        bath_temps.append(bath.current_water_temp)
        if bath.is_overflow():
            print("\nWater Overflow. Call the cops!")
            return
        bar.next()
    bar.finish()

def plotting1():
    p = figure(title="An example of PID", x_axis_label='n', y_axis_label='u_pid')
    p.line(range(N), u_PID, legend_label="u_PID", line_width=2)
    show(p)

def plotting2():
    p = figure(title="An example of PID", x_axis_label='n', y_axis_label='t_n')
    p.line(range(N), bath_temps, legend_label="Temp", line_width=2)
    show(p)


temp_pid()
plotting1()
plotting2()