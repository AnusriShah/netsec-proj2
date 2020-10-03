# build out necessary gadgets for libc functions

# head starts in ecx, move to edx
def move_head_into_edx():

# head is edx, eax is the value, moving eax into edx
def write_head():
    return '0x0007672a'
# assumes edx is head, eax is value and will store what is in head
def read_head():
    
def move_head_left():
    # no decrement for edx
    # may have to add FFFF thing to decrement
    # move edx into eax, decrement eax, move it back
    return ["0x00088f34", "0x0007bc64", ]
def move_head_right():
    return "0x0002d654"
def increment_reg(reg):
    if(reg == "eax"):
        return "0x000270ea"
    if(reg == "ebp"):
        return "0x00035832"
    if(reg == "ecx"):
        return "0x0002d216"
    if(reg == "edx"):
        return "0x0002d654"
    if(reg == "esi"):
        return "0x000651a6"
    if(reg == "esp"):
        return "0x00020668"  
def decrement_reg(reg):
    if(reg == "eax"):
        return "0x0007bc64"
    if(reg == "ebp"):
        return "0x0004c892"
    if(reg == "ecx"):
        return "0x0001e6f2"
    if(reg == "edi"):
        return "0x000472d4"
    if(reg == "esi"):
        return "0x0005118a"
    if(reg == "esp"):
        return "0x000ea6c7"
# register that stores the state - using esi       
def get_state():
    # maybe push onto stack?
    # TODO: figure out way
# EAX = EAX - ECX
def eax_minus_ecx():
    return "0x00150e98"
# EAX = EAX + ECX
def eax_plus_ecx():
    return "0x00098a40"     
def zero_out_reg(reg):
    if(reg == "eax"):
        return "0x0002ff9f" # xor eax, eax
    # for other registers, no xor command
    # TODO: figure out way to zero out others
# register value must be 0
def move_flags_eax(reg):
    # LAHF with RETF 0x0003b5d2 : lahf ; retf // 9fcb
    # TODO: CHECK IF RETF IS OK
    return "0x0003b5d2" # loads flags into EAX
def get_flags():
    return ""
# used neg instruction: negates a value by finding 2's complement of its single operand
# NEG AFFECTS FLAGS
def negate_reg(reg):
    # XOR it with FFFF?
    if(reg == "eax"):
        return "0x000654b0"
    if(reg == "edx"):
        return "0x0001b0ac"
def not_reg(reg):
    # TODO: not register
def pop_register(reg):
    if(reg == "eax"):
        return "0x00026687"
    if(reg == "ebp"):
        return "0x0001a4cc"
    if(reg == "ebx"):
        return "0x0001a8b5"
    if(reg == "edi"):
        return "0x00019173"
    if(reg == "edx"):
        return "0x0002effc"
    if(reg == "esi"):
        return "0x0001bf2c"
    if(reg == "esp"):
        return "0x001236b0"    
def and_eax_register(reg):
    if(reg == "ecx"):
        return "0x0002d87e"
    if(reg == "edx"):
        return "0x0002df2e" 
def swap_eax(reg):
def swap_two_regs(reg1, reg2):
def set_esp(reg):
# TODO: remove quotes above
def write_ecx_to_mem(mem_loc):
def jump(self, output):
    # mov eax into temp register (edi)
    output += "0x0002e745"
    output += "0x00019173"
    # sub eax, ecx
    output += "0x00150e98"
    # neg eax
    output += "0x000654b0"
    # add with carry (adc reg, reg)
    output += zero_out_reg("esi")
    output += "0x0007773c"
    # neg reg
    # mov esp_delta into temp register
    # and reg, esp_delta
    # add esp, reg
    # ret
def helper(helperOutput):
    # zero out ecx
    # run for loop
    helperOutput += read_head() # will store in eax
    helperOutput += zero_out_reg("ecx") # no zero out for ecx ATM
    for i in range(0, 100):
        for i in range(0, 255):
            # push tape value onto stack, push reg value onto stack, see if equal
            # use compare, if NE, JUMP
            # write to mem_location
            # compare EAX to every input symbol
            # need another register to hold state
            output += "0x0012a410" # TODO: trash other instructions in this cmp eax, ecx command
            # JUMP: JNE, push output byte (state, symbol, direction)
            # check the output byte - see if state is accept or reject
            # parse output byte
            state = ''
            if(state == 'r')
                print("Output Payload: ", output)
                exit(1) # put lib c instruction to exit
            if(state == 'a')
                print("Output Payload: ", output)
                exit(0) # put lib c instruction to exit
            # if reject, exit with 1
            # if accept, exit with 0
            # if neither, set output state (modify register esi - contains state)
                # move head in right direction based on output byte
                # start for loop again, zero out ecx
            # increment ecx
            # repeat whole loop
def main():
    # NOTE: will probably have to increment by 2 or 3 instead of 1 for mem location
        # bc we also have to include compare/jump instructions
        # compare sets the flag, JNE checks the flag
    # write input symbols into memory
    # loop from 0-100, 0-255 and every time, 
    # inc mem location and inc temp register
    # move register value to mem location
    # set register back to 0 once you exit inner loop
    output = ""
    output += move_head_into_edx()
    output += read_head() # will store in eax
    output += zero_out_reg("ecx") # no zero out for ecx ATM
    print(helper(output))



            
            

