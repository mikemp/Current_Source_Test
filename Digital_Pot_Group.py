'''
Created on Jan 17, 2015

@author: Michael Empey
'''

class Digital_Pot_Group:
    '''
    classdocs
    '''


    def __init__(self, ordered_array_of_potentiometers):
        '''
        Constructor
        '''
        self.variable_R_array = ordered_array_of_potentiometers
        self.num_pots = len(self.variable_R_array)
        # max number of wiper positions for a single potentiometer
        self.num_pos = self.variable_R_array[0].total_num_of_positions
        self.group_max_pos = self.num_pots*self.num_pos

        self.total_positions = 1

        for R in self.variable_R_array:
            self.total_positions += R.total_num_of_positions-1
        self.set_pos_to_min()


    def set_wiper_pos(self,pos):
        set_remain = (pos-self.num_pots)%(self.num_pos-self.num_pots)
        num_pots_full = (pos-self.num_pots)/(self.num_pos-self.num_pots)
        # print [pos, num_pots_full, set_remain]
        # print [self.num_pots, self.total_positions, pos]
        # print [pos <= self.total_positions, pos > self.num_pots]
        if pos <= self.total_positions and pos > self.num_pots:

            if num_pots_full > 0:
                for ii in range(0, num_pots_full):
                    self.variable_R_array[ii].set_max_pos()

            if num_pots_full < self.num_pots:
                for ii in range(num_pots_full,self.num_pots-1):
                    self.variable_R_array[ii].set_wiper_pos(1)
                if set_remain > 0:
                    self.variable_R_array[num_pots_full-1].set_wiper_pos(set_remain)


        elif pos == self.num_pots:
            for R in self.variable_R_array:
                R.set_wiper_pos(1)

        else:
            print [self.num_pots, self.total_positions, pos]
            raise IndexError('Position out of bounds, it does not fall in the range of positions')

        self.group_wiper_pos = pos
        return self

    def set_pos_to_max(self):
        self.set_wiper_pos(self.total_positions)
        return self

    def set_pos_to_min(self):
        self.set_wiper_pos(self.num_pots)
        return self

    def get_min_position(self):
        return self.num_pots

    def get_max_position(self):
        return self.group_max_pos

    def get_pots(self):
        return self.variable_R_array

    def get_ideal_value(self):
        sum = 0
        for R in self.variable_R_array:
            sum += R.get_ideal_value()
        return sum


    def can_increment(self):
        return self.group_wiper_pos < self.group_max_pos

    def increment(self):
        return self.set_wiper_pos(self.group_wiper_pos+1)

    def can_decrement(self):
        return self.group_wiper_pos > self.num_pots

    def decrement(self):
        return self.set_wiper_pos(self.group_wiper_pos-1)







