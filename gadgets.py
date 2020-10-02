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

def move_head_right():
    return '0x0002d654'
def increment_reg(reg):
    if(reg == "eax"):
        return '0x000270ea'
    if(reg == "ebp"):
        return '0x00035832'
    if(reg == "ecx"):
        return '0x0002d216'
    if(reg == "edx"):
        return '0x0002d654'
    if(reg == "esi"):
        return '0x000651a6'
    if(reg == "esp"):
        return '0x00020668'  
def decrement_reg(reg):
    if(reg == "eax"):
        return '0x0007bc64'
    if(reg == "ebp"):
        return '0x0004c892'
    if(reg == "ecx"):
        return '0x0001e6f2'
    if(reg == "edi"):
        return '0x000472d4'
    if(reg == "esi"):
        return '0x0005118a'
    if(reg == "esp"):
        return '0x000ea6c7'
# register that stores the state - using ecx but subject to change         
def get_state():
    # maybe push onto stack?
    # TODO: figure out way
# EAX = EAX - ECX
def eax_minus_ecx():
    return '0x00150e98'
# EAX = EAX + ECX
def eax_plus_ecx():
    return '0x00098a40'     
def zero_out_reg(reg):
    if(reg == "eax"):
        return '0x0002ff9f' # xor eax, eax
    # for other registers, no xor command
    # TODO: figure out way to zero out others
# register value must be 0
def move_flags_eax(reg):
    # LAHF with RETF 0x0003b5d2 : lahf ; retf // 9fcb
    # TODO: CHECK IF RETF IS OK
    return '0x0003b5d2' # loads flags into EAX
def get_flags():
    return ''
# used neg instruction: negates a value by finding 2's complement of its single operand
# NEG AFFECTS FLAGS
def negate_reg(reg):
    # XOR it with FFFF?
    if(reg == "eax"):
        return '0x000654b0'
    if(reg == "edx"):
        return '0x0001b0ac' 
def pop_register(reg):
    if(reg == "eax"):
        return '0x00026687'
    if(reg == "ebp"):
        return '0x0001a4cc'
    if(reg == "ebx"):
        return '0x0001a8b5'
    if(reg == "edi"):
        return '0x00019173'
    if(reg == "edx"):
        return '0x0002effc'
    if(reg == "esi"):
        return '0x0001bf2c'
    if(reg == "esp"):
        return '0x001236b0'    
def and_eax_register(reg):
    if(reg == "ecx"):
        return '0x0002d87e'
    if(reg == "edx"):
        return '0x0002df2e' 
def swap_eax(reg):
def swap_two_regs(reg1, reg2):
def set_esp(reg):