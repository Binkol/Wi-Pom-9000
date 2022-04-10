class Termostat:
    def __init__(self, hot, cold, flow_speed, hot_percentage): 
        #flow_speed l/min

        self.hot_water_temp = hot
        self.cold_water_temp = cold
        self.hot_percentage = hot_percentage
        self.cold_percentage = 1 - hot_percentage
        self.flow_speed = flow_speed/60
        self.mixed_water_temp = 0

    
    def change_hot_percentage(self, percentage):
        self.hot_percentage = percentage
        self.cold_percentage = 1 - percentage

    def update_water_temp(self,):
        m1 = self.hot_percentage
        m2 = self.cold_percentage
        t1 = self.hot_water_temp 
        t2 = self.cold_water_temp

        self.mixed_water_temp = (m1*t1 + m2*t2)/(m1+m2)