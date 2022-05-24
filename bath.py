class Bath:
    def __init__(self, start_water_temp, start_water_amount, smax_water_amount):
        self.current_water_temp = start_water_temp
        self.target_water_temp = 0
        self.amount_of_water = start_water_amount #liters
        self.max_water_amount = smax_water_amount #liters

    def is_overflow(self,):
        if self.amount_of_water < self.max_water_amount:
            return False
        return True
            

    def mix_waters(self, flow_speed, termostat_water_temp):
        #flow_speed - variable taken from Termostat object
        """
        :param flow_speed: import from Termostat.flow_speed
        :param termostat_water_temp: import from Termostat.mixed_water_temp
        :return: returns temperature of water in bath
        """ 
        m1 = flow_speed
        m2 = self.amount_of_water
        t1 = termostat_water_temp 
        t2 = self.current_water_temp

        self.current_water_temp = (m1*t1 + m2*t2)/(m1+m2)

    def update_water_amount(self, amount):
        """
        :param amount: import from Termostat.flow_speed
        """ 
        self.amount_of_water += amount
