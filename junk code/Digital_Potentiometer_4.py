'''
Created on Jan 15, 2015

@author: Michael Empey

Having a digital pot class and then creating a data structure to manage the 
different branches of the current source

So then the digital pot class only needs to be implemented for a single RDAC

'''

class Digital_Potentiometer_4:
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
        self.wiper_pos_RDAC0 = p
        self.wiper_pos_RDAC1 = p
        self.wiper_pos_RDAC2 = p
        self.wiper_pos_RDAC3 = p
        self.total_num_of_positions = ptot
        self.inverted = True

    def set_address_bit0(self, AD0):
        self.address_bit0 = AD0

    def set_address_bit1(self, AD1):
        self.address_bit1 = AD1

    def set_wiper_position_RDAC0(self, pos):
        self.wiper_pos_RDAC0 = pos

    def set_wiper_position_RDAC1(self, pos):
        self.wiper_pos_RDAC1 = pos
        
    def set_wiper_position_RDAC2(self, pos):
        self.wiper_pos_RDAC2 = pos
        
    def set_wiper_position_RDAC3(self, pos):
        self.wiper_pos_RDAC3 = pos

    def get_wiper_position_RDAC0(self):
        return self.wiper_pos_RDAC0

    def get_wiper_position_RDAC1(self):
        return self.wiper_pos_RDAC1

    def get_wiper_position_RDAC2(self):
        return self.wiper_pos_RDAC2

    def get_wiper_position_RDAC3(self):
        return self.wiper_pos_RDAC3

    def get_address_bits(self):
        return [self.address_bit1, self.address_bit0]

    def __get_ideal_value(self, wiper_pos):
        if self.inverted:
            return (self.total_num_of_positions-1-wiper_pos)*self.size/(self.total_num_of_positions-1)
        else:
            return wiper_pos*self.size/(self.total_num_of_positions-1)

    def get_ideal_value_RDAC0(self, wiper_pos):
        return self.__get_ideal_value(self.wiper_pos_RDAC0)

    def get_ideal_value_RDAC1(self, wiper_pos):
        return self.__get_ideal_value(self.wiper_pos_RDAC1)

    def get_ideal_value_RDAC2(self, wiper_pos):
        return self.__get_ideal_value(self.wiper_pos_RDAC2)

    def get_ideal_value_RDAC3(self, wiper_pos):
        return self.__get_ideal_value(self.wiper_pos_RDAC3)

    def get_address_byte(self,W_R):
        address = '01011%d%d%d' % (self.address_bit1,self.address_bit1,W_R)
        return int(address,2)
    
    def get_instruction_byte(self,A1,A0,CMD_REG=0,EE_RDAC=0):
        instruction = '%d0%d000%d%d' % (CMD_REG,EE_RDAC,A1,A0)
        return int(instruction, 2)

    def get_data_byte(self):
        return self.wiper_pos

    def __I2C_write_command(self,A1,A0):
        return [self.get_address_byte(0),self.get_instruction_byte(A1,A0),self.get_data_byte()]

    def I2C_write_command_RDAC0(self):
        return self.__I2C_write_command(0,0)

    def I2C_write_command_RDAC1(self):
        return self.__I2C_write_command(0,1)

    def I2C_write_command_RDAC2(self):
        return self.__I2C_write_command(1,0)

    def I2C_write_command_RDAC3(self):
        return self.__I2C_write_command(1,1)
        
    def I2C_set_all_pots(self, pos):
        self.set_wiper_position(pos)
        return self.get_I2C_write_command()


