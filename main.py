from termostat import Termostat
from bath import Bath
import math
import time
termo = Termostat(60, 15, 13, 1) 
bath = Bath(20, 5)

for _ in range(100):
    termo.update_water_temp()
    bath.mix_waters(termo.flow_speed, termo.mixed_water_temp)
    bath.update_water_amount(termo.flow_speed)

    a = '{0:.3g}'.format(termo.mixed_water_temp)
    b = '{0:.3g}'.format(bath.current_water_temp)
    c = '{0:.3g}'.format(bath.amount_of_water)
    
    print(a, b, c)
    time.sleep(1)