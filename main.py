from termostat import Termostat
from bath import Bath
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure, show
from progress.bar import Bar
import skfuzzy.control as ctrl


temp_0 = 20 #water temperature at start
temp_target = 35

Tp = 0.1 #okres próbkowania 
t_sim = 1 * 3600
N = int(t_sim/Tp) 

kp = 0.2 #wzmocnienie regulatora
Ti = 7.5 #czas zdwojenia
Td = 0.2

termo = Termostat(60, 10, 5, 0.6) #(hot, cold, flow_spped, hot_percentage)
bath = Bath(temp_0, 1, 400)       #(start_water_temp, start_water_amount, smax_water_amount)
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


def fuzzyInit():

        universe = np.linspace(-3, 4, 1)
        error = ctrl.Antecedent(universe, 'error')
        errorSum = ctrl.Antecedent(universe, 'errorSum')
        output = ctrl.Consequent(universe, 'output')

        names = ['nb', 'ns', 'ze', 'ps', 'pb']

        error.automf(names=names)
        errorSum.automf(names=names)
        output.automf(names=names)

        rule0 = ctrl.Rule(antecedent=((error['nb'] & errorSum['nb']) |
                                      (error['ns'] & errorSum['nb']) |
                                      (error['nb'] & errorSum['ns'])),
                          consequent=output['nb'], label='rule nb')

        rule1 = ctrl.Rule(antecedent=((error['nb'] & errorSum['ze']) |
                                      (error['nb'] & errorSum['ps']) |
                                      (error['ns'] & errorSum['ns']) |
                                      (error['ns'] & errorSum['ze']) |
                                      (error['ze'] & errorSum['ns']) |
                                      (error['ze'] & errorSum['nb']) |
                                      (error['ps'] & errorSum['nb'])),
                          consequent=output['ns'], label='rule ns')

        rule2 = ctrl.Rule(antecedent=((error['nb'] & errorSum['pb']) |
                                      (error['ns'] & errorSum['ps']) |
                                      (error['ze'] & errorSum['ze']) |
                                      (error['ps'] & errorSum['ns']) |
                                      (error['pb'] & errorSum['nb'])),
                          consequent=output['ze'], label='rule ze')

        rule3 = ctrl.Rule(antecedent=((error['ns'] & errorSum['pb']) |
                                      (error['ze'] & errorSum['pb']) |
                                      (error['ze'] & errorSum['ps']) |
                                      (error['ps'] & errorSum['ps']) |
                                      (error['ps'] & errorSum['ze']) |
                                      (error['pb'] & errorSum['ze']) |
                                      (error['pb'] & errorSum['ns'])),
                          consequent=output['ps'], label='rule ps')

        rule4 = ctrl.Rule(antecedent=((error['ps'] & errorSum['pb']) |
                                      (error['pb'] & errorSum['pb']) |
                                      (error['pb'] & errorSum['ps'])),
                          consequent=output['pb'], label='rule pb')

        system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])
        sim = ctrl.ControlSystemSimulation(system)
        return sim

def temp_fuzzy():
    sim = fuzzyInit()

    temp_plot = []
    u_plot = []
    #e = []

    #current_temp = 0 #mamy w bath
    #time = 0 # idk po co to 
    I = 0
    #u_max = 10
    #u_min = 0
    #delta_u = Tp 
    
    for i in range(N - 1):
        temp_plot.append(bath.current_water_temp)

        e.append(temp_target - bath.current_water_temp)

        #print(I, e[-1])

        I = I + e[-1] #zamienic na zmiane uchybu
        #I =  e[-2] + e[-1]
        sim.input['error'] = e[-1]
        sim.input['errorSum'] = I * Tp
        sim.compute()

        u_plot.append(kp * sim.output['output'])

        if u_plot[-1] <= u_max and u_plot[-1] >= u_min:
            termo.change_hot_percentage(u_plot[-1]/u_max)
        elif u_plot[-1] > u_max:
            termo.change_hot_percentage(1.0)
        else:
            termo.change_hot_percentage(u_min)


        termo.update_water_temp()
        bath.mix_waters(Tp, termo.flow_speed, termo.mixed_water_temp)
        bath.update_water_amount(Tp, termo.flow_speed)
    
    return temp_plot, u_plot





def plotting1():
    p = figure(title="An example of PID", x_axis_label='n', y_axis_label='u_pid')
    p.line(range(N), u_PID, legend_label="u_PID", line_width=2)
    show(p)

def plotting2():
    p = figure(title="An example of PID", x_axis_label='n', y_axis_label='t_n')
    p.line(range(N), bath_temps, legend_label="Temp", line_width=2)
    show(p)


def plotting3(plot_values, plot_title):
    p = figure(title=plot_title, x_axis_label='n', y_axis_label='t_n')
    p.line(range(N), plot_values, legend_label="Temp", line_width=2)
    show(p)


temp_pid()
plotting1()
plotting2()

#temp_plot, u_plot = temp_fuzzy()
#plotting3(temp_plot, "temp_plot")
#plotting3(u_plot, "u_plot")