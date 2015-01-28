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
        self.min_position = len(self.variable_R_array)
        self.total_positions = 1
        for R in self.variable_R_array:
            self.total_positions += R.total_num_of_positions-1
        self.set_pos_to_min(self)


    def set_wiper_pos(self,pos):
        if pos >= self.min_position and pos <= self.total_positions:
            self.group_wiper_pos = pos
            for R in self.variable_R_array:
                if pos > R.total_num_of_positions:
                    pos -= R.total_num_of_positions
                    R.set_wiper_pos(R.total_num_of_positions)
                else:
                    R.set_wiper_pos()
        else:
            raise IndexError('Position out of bounds, it does not fall in the range of positions')
        return self.group_wiper_pos
    
    def set_pos_to_max(self):
        self.set_wiper_pos(self.total_positions)
        return self.group_wiper_pos
    
    def set_pos_to_min(self):
        self.set_wiper_pos(self.min_position)
        return self.group_wiper_pos 
            
    def get_min_position(self):
        return self.min_position
    
    def get_max_position(self):
        return self.total_positions
            
    def can_increment(self):
        return False
    
    def increment(self):
        return self.group_wiper_pos
    
    def can_decrement(self):
        return False
    
    def decrement(self):
        return self.group_wiper_pos
    
    

        
        
        
        