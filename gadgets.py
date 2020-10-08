import sys

class ROP:
    #TODO: int 0x80: 10a82
    #TODO: add libc offset: 0xb7dec000
    #TODO: set /proc/sys/kernel/randomize_va_space to 0
    # head starts in ecx, move to edx
    #******FIX*******
    def initialize_head_state(self):
        # initialize head
        tempOutput += 0x0002effc.to_bytes(4, byteorder='little') # pop edx
        tempOutput += 0x0008ae23.to_bytes(4, byteorder='little') # push ecx -> NEED TO FIX THIS
        return tempOutput

    # head is edx, eax is the value, moving eax into edx
    def write_head(self, num):
        tempOutput += self.pop_register("eax")
        tempOutput += num
        tempOutput += 0x0007672a.to_bytes(4, byteorder='little') # mov dword ptr [edx], eax ; ret
        return tempOutput

    # assumes edx is head, eax is value and will store what is in head
    def read_head(self):
        # move at address of edx into eax
        return 0x0006a227.to_bytes(4, byteorder='little') # mov eax, dword ptr [edx] ; ret

    def move_head_left(self):
        # no decrement for edx
        # may have to add FFFF thing to decrement
        # move edx into eax, decrement eax, move it back
        tempOutput = 0x00088f34.to_bytes(4, byteorder='little') # 0x00088f34 : mov eax, edx; ret
        tempOutput += 0x0007bc64.to_bytes(4, byteorder='little') # 0x0007bc64 : dec eax; ret
        tempOutput += 0x00121c7d.to_bytes(4, byteorder='little') # 0x00121c7d : mov edx, eax ; mov eax, edx ; ret
        return tempOutput

    def move_head_right(self):
        #NOTE: ADDED NOPS TO BALANCE W/ MOVE_HEAD_LEFT - think this works?
        tempOutput = 0x0002d654.to_bytes(4, byteorder='little') # : inc edx ; ret
        tempOutput += 0x0001a8bf.to_bytes(4, byteorder='little') #nops
        tempOutput += 0x0001a8bf.to_bytes(4, byteorder='little')
        tempOutput += 0x0001a8bf.to_bytes(4, byteorder='little')
        tempOutput += 0x0001a8bf.to_bytes(4, byteorder='little')
        return tempOutput

    def increment_reg(self, reg):
        if(reg == "eax"):
            return 0x000270ea.to_bytes(4, byteorder='little')
        if(reg == "ebp"):
            return 0x00035832.to_bytes(4, byteorder='little')
        if (reg == "ebx"):
            return 0x0002d216.to_bytes(4, byteorder='little')
        if(reg == "edx"):
            return 0x0002d654.to_bytes(4, byteorder='little')
        if(reg == "esi"):
            return 0x000651a6.to_bytes(4, byteorder='little')
        if(reg == "esp"):
            return 0x00020668.to_bytes(4, byteorder='little')  

    def decrement_reg(self, reg):
        if(reg == "eax"):
            return 0x0007bc64.to_bytes(4, byteorder='little')
        if(reg == "ebp"):
            return 0x0004c892.to_bytes(4, byteorder='little')
        if(reg == "ecx"):
            return 0x0001e6f2.to_bytes(4, byteorder='little')
        if(reg == "edi"):
            return 0x000472d4.to_bytes(4, byteorder='little')
        if(reg == "esi"):
            return 0x0005118a.to_bytes(4, byteorder='little')
        if(reg == "esp"):
            return 0x000ea6c7.to_bytes(4, byteorder='little')      

    
    def eax_minus_ecx(self):
        # EAX = EAX - ECX
        return 0x00150e98.to_bytes(4, byteorder='little')

    def eax_plus_ecx(self):
        # EAX = EAX + ECX
        return 0x00098a40.to_bytes(4, byteorder='little')   

    def xchg_w_eax(self, reg):
        if (reg == "ebp"):
            return 0x0002d455.to_bytes(4, byteorder='little')
        if (reg == "ebx"):
            return 0x000f99df.to_bytes(4, byteorder='little')
        if (reg == "ecx"):
            #TRASHES ECX: xchg eax, ecx ; and al, 0x5b ; ret
            return 0x0002664e.to_bytes(4, byteorder='little')
        if (reg == "edi"):
            return 0x00020a3d.to_bytes(4, byteorder='little')
        if (reg == "edx"):
            return 0x00041702.to_bytes(4, byteorder='little')
        if (reg == "esi"):
            return 0x0001b286.to_bytes(4, byteorder='little')
        if (reg == "esp"):
            return 0x0001b269.to_bytes(4, byteorder='little')

    def swp_regs(self, reg1, reg2):
        output = self.xchg_w_eax(reg1)
        output += self.xchg_w_eax(reg2)
        output += self.xchg_w_eax(reg1)

    def zero_out_reg(self, reg):
        if(reg == "eax"):
            return 0x0002ff9f.to_bytes(4, byteorder='little') # xor eax, eax
        else: 
            tempOutput = self.xchg_w_eax(reg)
            tempOutput += self.zero_out_reg("eax")
            tempOutput += self.xchg_w_eax(reg)
            return tempOutput
   
    def move_flags_eax(self, reg):
         # register value must be 0
        # NOTE: probably don't need so ignore issues for time being
        # LAHF with RETF 0x0003b5d2 : lahf ; retf // 9fcb
        # TODO: CHECK IF RETF IS OK
        return 0x0003b5d2.to_bytes(4, byteorder='little') # loads flags into EAX
    
    def negate_reg(self, reg): # use negate when we want to use carry flag in jump function
        # negates a value by finding 2's complement of its single operand
        # NEG AFFECTS FLAGS
        if(reg == "eax"):
            return 0x000654b0.to_bytes(4, byteorder='little')
        if(reg == "edx"):
            return 0x0001b0ac.to_bytes(4, byteorder='little')

    #TODO: DELETE THIS LATER
    def push_register(self, reg):
        if(reg == "eax"):
            return 0x0002e745.to_bytes(4, byteorder='little')
        if (reg == "ecx"):
            #0x0008ae23 : push ecx ; add al, 0x5b ; ret // TRASHES EAX
            return 0x0008ae23.to_bytes(4, byteorder='little')
        if(reg == "edi"):
            return 0x000e5705.to_bytes(4, byteorder='little')
        if(reg == "edx"):
            return 0x00158848.to_bytes(4, byteorder='little')
        if(reg == "esi"):
            return 0x000603c5.to_bytes(4, byteorder='little')
        if(reg == "esp"):
            return 0x00137dd6.to_bytes(4, byteorder='little')
        if(reg == "ebx"): # will trash eax; 0x000c78c1 : push ebx ; or al, 0x83 ; ret; OR's al
            return 0x000c78c1.to_bytes(4, byteorder='little')

    def pop_register(self, reg):
        if(reg == "eax"):
            return 0x00026687.to_bytes(4, byteorder='little')
        if(reg == "ebp"):
            return 0x0001a4cc.to_bytes(4, byteorder='little')
        if(reg == "ebx"):
            return 0x0001a8b5.to_bytes(4, byteorder='little')
        if(reg == "edi"):
            return 0x00019173.to_bytes(4, byteorder='little')
        if(reg == "edx"):
            return 0x0002effc.to_bytes(4, byteorder='little')
        if(reg == "esi"):
            return 0x0001bf2c.to_bytes(4, byteorder='little')
        if(reg == "esp"):
            return 0x001236b0.to_bytes(4, byteorder='little') 
        if (reg == "ecx"):
            tempOutput = self.xchg_w_eax("ecx")
            tempOutput += self.pop_register("eax")
            tempOutput += self.xchg_w_eax("ecx")
            return tempOutput

    def and_eax_register(self, reg):
        if(reg == "ecx"):
            return 0x0002d87e.to_bytes(4, byteorder='little')
        if(reg == "edx"):
            return 0x0002df2e.to_bytes(4, byteorder='little') 

    def add_eax_to_edx(self):
        # 0x00121c91 : add edx, eax ; pop ebx ; pop esi ; mov eax, edx ; ret
        #TODO: FIX THE PUSH
        tempOutput = self.push_register("esi")
        tempOutput += 0x0012e414.to_bytes(4, byteorder='little') # push random instead of pushing ebx; push 0x1185f89
        tempOutput += 0x00121c91.to_bytes(4, byteorder='little') # add edx, eax
        return tempOutput

    def jump(self):
        #print("in jump")
        # copy eax into temp register (edi)
        #TODO: FIX THE PUSH
        output = self.push_register("eax")
        output += self.pop_register("edi")
        #sub eax, ecx
        output += 0x00150e98.to_bytes(4, byteorder='little')
        # neg eax
        output += 0x000654b0.to_bytes(4, byteorder='little')
        # add with carry (adc reg, reg)
        output += self.zero_out_reg("esi")
        output += 0x0007773c.to_bytes(4, byteorder='little')
        # push esi, pop eax
        output += self.xchg_w_eax("esi")
        # neg eax
        output += self.negate_reg("eax")
        #save edx (head) in esi, bc need to use edx for esp_delta
        output += self.swp_regs("esi", "edx")
        # now: esi has edx value, AKA head; edi has eax AKA input symbol

        #TODO: PUT ESP_DELTA INTO EDX
        # esp_delta = 74 -> change this
        output += self.pop_register("edx")
        output += 0x4a.to_bytes(4, byteorder='little')
        # and eax, esp_delta
        output += self.and_eax_register("edx") # and eax, edx (esp_delta)

        #increment counter before jump
        output += self.increment_reg("ecx")

        # eax has esp_delta, need to add esp, eax
        # TODO: can't use xchg with this and can't use push...FIX!! 
        output += self.push_register("esp")
        output += self.pop_register("edx")
        output += self.add_eax_to_edx()
        output += self.push_register("edx")
        output += self.pop_register("esp")
        return output

    def helper(self, helperOutput, scan, length):
        #print("in helper")
        helperOutput += self.read_head() # will store in eax 
        #NOTE: this only works if read_head() only overwrites the lower 8 bits of eax - think we need to fix this!!!!!
        #eax has input symbol 

        # zero out ecx for counter;
        helperOutput += self.zero_out_reg("ecx")

        #TODO: change code to compare eax (state/symbol) & ecx (counter)
        for i in range(0, length):
            helperOutput += self.jump()
            # restore registers: esi to edx, edi to eax
            helperOutput += self.xchg_w_eax("edi")
            helperOutput += self.swp_regs("esi", "edx")

            output = scan.readline()
            #print(output)
            outputArr = output.split(" ")
            helperOutput += self.write_head(outputArr[3])
            # check for accept/reject state. else, call helper again
            #print(outputArr[2])
            if (outputArr[2] == 'r'):
                #print("reject")
                helperOutput += self.pop_register("eax")
                helperOutput += 0x00000001.to_bytes(4, byteorder='little')      # pop 1 into eax for exit code
                helperOutput += 0x10a82.to_bytes(4, byteorder='little')         #int 0x80 in libc
            
            elif (outputArr[2] == 'a'):
                #print("accept")
                helperOutput += self.pop_register("eax")
                helperOutput += 0x00000000.to_bytes(4, byteorder='little')      # pop 0 into eax for exit code
                helperOutput += 0x10a82.to_bytes(4, byteorder='little')

            else:
                helperOutput += self.zero_out_reg("ecx")        
                helperOutput += self.pop_register("eax")
                helperOutput += outputArr[2].to_bytes(4, byteorder='little')      #pop output state into eax
                helperOutput += 0x0006ea87.to_bytes(4, byteorder='little')        #or ch, al ; ret
                #at this point, the new state is in ch, need to move to ah, al is 0
                helperOutput += self.xchg_w_eax("ecx")
                #check direction
                if(outputArr[4] == 'R'):
                    helperOutput += self.move_head_right()
                else:
                    helperOutput += self.move_head_left()
                #helperOutput = self.helper(helperOutput, scan, length)
                #return self.helper(helperOutput, scan, length)
        return helperOutput
        
    def main(self, filename):
        #COUNTER: ECX
        output = self.initialize_head_state()
        output += self.zero_out_reg("eax")
        #output += self.zero_out_reg("ecx") 
        input_ = open(filename, 'r')
        inputLines = input_.readlines()
        length = len(inputLines)
        input_.close()
        scan = open(filename, 'r')
        output += self.helper(output, scan, length)
        sys.stdout.buffer.write(output)
a = ROP()
a.main("testing.txt")


            
            

