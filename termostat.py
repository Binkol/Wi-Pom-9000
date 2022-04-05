class Termostat:
    def __init__(self, hot, cold, flow_speed, hot_percentage):
        self.hot_water_temp = hot
        self.cold_water_temp = cold
        self.hot_percentage = hot_percentage
        self.cold_percentage = 100 - hot_percentage
        self.flow_speed = flow_speed
        self.mixed_water_temp = 0

    
    def change_hot_percentage(self, percentage):
        self.hot_percentage = percentage
        self.cold_percentage = 100 - percentage

    def update_water_temp(self,):
        pass