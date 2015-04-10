'''
Created on Feb 7, 2015

@author: mikemp
'''

from Digital_Potentiometer import *
from Digital_Pot_Group import *

R1 = Digital_Potentiometer(0, 0, 0, 0, 1E3)
R2 = Digital_Potentiometer(0, 0, 0, 1, 1E3)
R3 = Digital_Potentiometer(0, 0, 1, 0, 1E3)
R4 = Digital_Potentiometer(0, 0, 1, 1, 1E3)

R5 = Digital_Potentiometer(0, 1, 0, 0, 1E3)
R6 = Digital_Potentiometer(0, 1, 0, 1, 1E3)
R7 = Digital_Potentiometer(0, 1, 1, 0, 1E3)
R8 = Digital_Potentiometer(0, 1, 1, 1, 1E3)

R9  = Digital_Potentiometer(1, 1, 0, 0, 1E3)
R10 = Digital_Potentiometer(1, 1, 0, 1, 1E3)
R11 = Digital_Potentiometer(1, 1, 1, 0, 1E3)
R12 = Digital_Potentiometer(1, 1, 1, 1, 1E3)

RG1 = Digital_Pot_Group([R1,R2,R3,R4])
RG2 = Digital_Pot_Group([R5,R6,R7,R8])

''' UTILITY FUNCTIONS '''
def i2c_group_print_data(pot_group):
    pot_array = pot_group.get_pots()
    ic2_command = []
    for pot in pot_array:
        ic2_command.append([hex(x) for x in pot.I2C_set_command()])
    print ic2_command

if __name__ == '__main__':
    
    print [RG2.get_min_position(),RG2.get_max_position()]
    
    RG2.set_pos_to_min()
    for ii in RG2.iterator():
        RG2.set_wiper_pos(ii)
        print [ii,RG2.get_ideal_value()]
        i2c_group_print_data(RG2)
        
        
    
#     RG2.set_pos_to_min()
#     ii = 0
#     while True:
#         i2c_group_print_data(RG2)
#         if not RG2.can_increment():
#             break
#         else:
#             RG2.increment()
#             ii += 1
        

