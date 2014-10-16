'''
Created on Oct 14, 2014

@author: mikemp
'''

class Digital_Potentiometer:
    '''
    classdocs
    '''


    def __init__(self, AD0, AD1, reg_bit, size=1e3, ptot=256, p=0):
        '''
        Constructor
        '''
        self.address_bit0 = AD0
        self.address_bit1 = AD1
        self.register_bit = reg_bit
        self.size = size
        self.wiper_pos = p
        self.total_num_of_positions = ptot
        self.inverted = True
        
    def set_address_bit0(self, AD0):
        self.address_bit0 = AD0
    
    def set_address_bit1(self, AD1):
        self.address_bit1 = AD1
    
    def set_register_bit(self, bit):
        self.register_bit = bit
    
    def set_wiper_position(self, pos):
        self.wiper_pos = pos
    
    def get_address_bits(self):
        return [self.address_bit1, self.address_bit0]
    
    def get_register_bit(self):
        return self.register_bit
    
    def get_wiper_position(self):
        return self.wiper_pos
    
    def get_ideal_value(self):
        if self.inverted
            return (self.total_num_of_positions-1-self.wiper_pos)*self.size/(self.total_num_of_positions-1)
        else:
            return self.wiper_pos*self.size/(self.total_num_of_positions-1)
    
    def get_address_byte(self,W_R):
        address = '01011%d%d%d' % (self.address_bit1,self.address_bit1,W_R)
#         return "0x{:02x}".format(int(address,2))
#         return hex(int(address,2))
        return int(address,2)
    
    def get_instruction_byte(self):
        instruction = '%d0000000' % (self.register_bit)
#         return "0x{:02x}".format(int(instruction, 2))
#         return hex(int(instruction, 2))
        return int(instruction, 2)
    
    def get_data_byte(self):
#         return "0x{:02x}".format(self.wiper_pos)
#         return hex(self.wiper_pos)
        return self.wiper_pos
    
    def get_I2C_write_command(self):
        return [self.get_address_byte(0),self.get_instruction_byte(),self.get_data_byte()]
    
    def I2C_set_value(self, pos):
        self.set_wiper_position(pos)
        return self.get_I2C_write_command()
        
        