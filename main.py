from termostat import Termostat
from bath import Bath
import matplotlib.pyplot as plt
import numpy as np
import time
from bokeh.plotting import figure, show

#TODO zmniejszyć okres próbkowania #mamy
#TODO napisac funkcje w Termostacie, która przyjmuje sygnał sterujący jako parametr do sterowania procentem hot/cold
#TODO dopasować wartość sygnalu steorwania do wartości przyjmowanej przez termostat czyli od 0.0 do 1.0


temp_0 = 20 #water temperature at start
temp_target = 38

Tp = 0.1 #okres próbkowania 
t_sim = 1.5 * 3600
N = int(t_sim/Tp) 

kp = 0.15 #wzmocnienie regulatora
Ti = 7.5 #czas zdwojenia
Td = 0.0

termo = Termostat(60, 10, 15, 0.6) #(hot, cold, flow_spped, hot_percentage)
bath = Bath(temp_0, 0.10, 300)       #(start_water_temp, start_water_amount, smax_water_amount)
counter = 0

u_PID = [0.5, ]
bath_temps = []
alpha = [0.5, ]
e = [0.0, ]

def temp_pid():
    global u_PID
    for i in range(N - 1):
        e.append(temp_target - bath.current_water_temp)
        u_PID.append(kp * (e[i] + Tp * sum(e) / Ti + Td * (e[i] - e[i-1]) / Tp))
        
        #print(u_PID[-1])
        if u_PID[-1] >= 1.0:
            termo.change_hot_percentage(1.0)
        elif u_PID[-1] <= 0:
            termo.change_hot_percentage(0)
        else:
            termo.change_hot_percentage(u_PID[-1])

        termo.update_water_temp()
        bath.mix_waters(Tp, termo.flow_speed, termo.mixed_water_temp)
        bath.update_water_amount(termo.flow_speed)


        bath_temps.append(bath.current_water_temp)
        #print("e: {}, temp_target: {} u_PID: {}, temp_t: {}".format(e[-1], temp_target, u_PID[i], termo.mixed_water_temp))

    print("e:",e[1:10])
    print("u_PID:",u_PID[1:10])

def plotting1():
    p = figure(title="An example of PID", x_axis_label='n', y_axis_label='t_n')
    p.line(range(N), u_PID, legend_label="u_PID", line_width=2)
    show(p)

def plotting2():
    p = figure(title="An example of PID", x_axis_label='n', y_axis_label='t_n')
    p.line(range(N), bath_temps, legend_label="Temp", line_width=2)
    show(p)


#print("It took {} seconds".format(counter))
temp_pid()
plotting1()
#plotting2()