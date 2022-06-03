from termostat import Termostat
from bath import Bath
import matplotlib.pyplot as plt
import numpy as np
import time
from bokeh.plotting import figure, show

#TODO zmniejszyć okres próbkowania #mamy
#TODO napisac funkcje w Termostacie, która przyjmuje sygnał sterujący jako parametr do sterowania procentem hot/cold
#TODO dopasować wartość sygnalu steorwania do wartości przyjmowanej przez termostat czyli od 0.0 do 1.0


temp_0 = 10 #water temperature at start
temp_target = 25

Tp = 0.1 #okres próbkowania 
t_sim = 1000
N = int(t_sim/Tp)

kp = 0.02 #wzmocnienie regulatora
Ti = 20 #czas zdwojenia
Td = 0.2

termo = Termostat(60, 10, 13, 0.6) #(hot, cold, flow_spped, hot_percentage)
bath = Bath(temp_0, 10, 300)       #(start_water_temp, start_water_amount, smax_water_amount)
counter = 0

bath_temps = []
data = []

def temp_pid():
    global bath_temps
    e = []
    bath_temps.append(0.6)
    for i in range(N - 1):
        # print(i)
        e.append(0.6)#temp_target - bath_temps[i])
        e_sum = sum(e)
        t_n = kp * (e[i] + (Tp / Ti * e_sum) + (Td / Tp * (e[i] - e[i - 1])))
        bath_temps.append(round(t_n, 3))
        termo.change_hot_percentage(round(t_n, 3))
        data.append([bath.current_water_temp, round(t_n, 3), termo.mixed_water_temp])

        termo.update_water_temp()
        bath.mix_waters(termo.flow_speed, termo.mixed_water_temp)
        bath.update_water_amount(termo.flow_speed)
        #print(t_n)



# while((bath.current_water_temp < temp_target) and not bath.is_overflow()):
#     termo.update_water_temp()
#     bath.mix_waters(termo.flow_speed, termo.mixed_water_temp)
#     bath.update_water_amount(termo.flow_speed)

#     a = '{0:.3g}'.format(termo.mixed_water_temp)
#     b = '{0:.3g}'.format(bath.current_water_temp)
#     c = '{0:.3g}'.format(bath.amount_of_water)
    
#     #print(a, b, c)

#     counter += 1


def plotting():
    p = figure(title="An example of PID", x_axis_label='n', y_axis_label='t_n')
    p.line(range(N), bath_temps, legend_label="Temp", line_width=2)
    show(p)


#print("It took {} seconds".format(counter))
temp_pid()
plotting()

#for x in data:
#    print(x)