#!/usr/bin/python
# -*- coding: latin-1 -*-
#--------------------------
# Module stack
# Author: Rodrigo Peixoto
#--------------------------

from exceptions  import Exception
from myhdl import *
from registrador import *
from mux2 import *

def stack( clk, reset, enable, push_pop, input_stack_1, output_stack_1, output_stack_2 ):

    reg_1_out, reg_2_out, mux_1_out, mux_2_out = [Signal( intbv( 0 )[32:] ) for i in range( 4 )]
    output_stack_1 = reg_1_out
    output_stack_2 = reg_2_out
    inside_clear = Signal( bool( 0 ) )

    instance_1 = mux2( a=input_stack_1, b=reg_2_out, sel=push_pop, result=mux_1_out )
    instance_2 = registrador( clk=clk, input_1=mux_1_out, enable=enable, clear=inside_clear, output_1=reg_1_out )
    instance_3 = mux2( a=reg_1_out, b=0, sel=push_pop, result=mux_2_out )
    instance_4 = registrador( clk=clk, input_1=mux_2_out, enable=enable, clear=inside_clear, output_1=reg_2_out )

    @always( clk.posedge )
    def process1():
        if reset:
            inside_clear.next = 1
        else:
            inside_clear.next = 0

    return process1, instance_1, instance_2#, instance_3, instance_4

if __name__ == '__main__':
    clk, reset, enable, push_pop = [Signal( bool( 0 ) ) for i in range( 4 )]
    input_1, output_1, output_2 = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]
    toVerilog( stack, clk, reset, enable, push_pop, input_1, output_1, output_2 )
