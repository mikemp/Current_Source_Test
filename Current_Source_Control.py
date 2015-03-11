'''
Created on Mar 10, 2015

@author: Michael Empey
'''

import sys, time

if __name__ == '__main__':
    pass

    set_current = 2 
    current_out = 0.001
    
    while True:
        time.sleep(0.010)
        print current_out
        err = set_current - current_out
        if current_out == set_current:
            break
        else:
            if err < 0:
                current_out -= 0.010
            if err > 0:
                current_out += 0.030
            
            
        
    