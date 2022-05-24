from termostat import Termostat
from bath import Bath
import matplotlib.pyplot as plt
import numpy as np
import time


#h_0 = 10 #water temperature at start
#h_target = 57

termo = Termostat(60, 10, 13, 0.6) 
bath = Bath(20, 10, 300)
target_temp = 57
counter = 0


# def height_pid():
#     global h
#     e = []
#     h.append(h_0)
#     for i in range(N - 1):
#         # print(i)
#         e.append(h_target - h[i])
#         e_sum = sum(e)
#         h_n = kp * (e[i] + (Tp / Ti * e_sum) + (Td / Tp * (e[i] - e[i - 1])))
#         h.append(h_n)



while((bath.current_water_temp < target_temp) and not bath.is_overflow()):
    termo.update_water_temp()
    bath.mix_waters(termo.flow_speed, termo.mixed_water_temp)
    bath.update_water_amount(termo.flow_speed)

    a = '{0:.3g}'.format(termo.mixed_water_temp)
    b = '{0:.3g}'.format(bath.current_water_temp)
    c = '{0:.3g}'.format(bath.amount_of_water)
    
    print(a, b, c)

    counter += 1

print()
print("It took {} seconds".format(counter))