'''
Created on Jan 15, 2015

@author: Michael Empey

'''

class Digital_Potentiometer:
    '''
    classdocs
    '''


    def __init__(self, AD1, AD0, A1, A0, size=1e3, ptot=256, p=1):
        '''
        Constructor
        '''
        self.address_bit1 = AD1
        self.address_bit0 = AD0
        self.register_bit1 = A1
        self.register_bit0 = A0
        self.size = size
        self.wiper_pos = p
        self.total_num_of_positions = ptot
        self.set_wiper_pos(p)
        self.inverted = False

    def set_wiper_pos(self,pos):
        # print [self.total_num_of_positions, pos]
        if pos >= 1 and pos <= self.total_num_of_positions:
            self.wiper_pos = pos
        else:
            raise IndexError('Position out of bounds, it does not fall in the range of positions')

    def set_max_pos(self):
        self.set_wiper_pos(self.total_num_of_positions)

    def set_inverted(self,inv=False):
        self.inverted = inv

    def get_wiper_pos(self):
        return self.wiper_pos

    def get_inverted(self):
        return self.inverted

    def get_ideal_value(self):
        if self.inverted:
            return (self.total_num_of_positions-1-self.wiper_pos)*self.size/(self.total_num_of_positions-1)
        else:
            return self.wiper_pos*self.size/(self.total_num_of_positions-1)

    def get_address_byte(self,W_R):
        address = '01011%d%d%d' % (self.address_bit1,self.address_bit0,W_R)
        return int(address,2)

    def get_instruction_byte(self,CMD_REG=0,EE_RDAC=0):
        instruction = '%d0%d000%d%d' % (CMD_REG,EE_RDAC,self.register_bit1,self.register_bit0)
        return int(instruction, 2)

    def get_data_byte(self):
        return self.wiper_pos-1

    def I2C_set_command(self):
        return [self.get_address_byte(0),self.get_instruction_byte(),self.get_data_byte()]


