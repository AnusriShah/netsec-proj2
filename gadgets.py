class ROP:
    # build out necessary gadgets for libc functions
    # TODO: add in self and say self.()
    # head starts in ecx, move to edx
    # TODO: everytime we do output += we add base address too "0xb7deb000" + 
    def initialize_head_state(self):
        # initialize head
        tempOutput = "0x0008ae23" # push ecx
        tempOutput += "0x0002effc" # pop edx
        return tempOutput
    # head is edx, eax is the value, moving eax into edx
    def write_head(self, num):
        #TODO:*********unsure if this is allowed**********
        tempOutput = num
        tempOutput += self.pop_register("eax")
        tempOutput += "0x0007672a" # mov dword ptr [edx], eax ; ret
        return tempOutput
        # TODO: may have to swap pop and num depending on what order of arguments are
    # assumes edx is head, eax is value and will store what is in head
    def read_head(self):
        # move at address of edx into eax
        return "0x0006a227" # mov eax, dword ptr [edx] ; ret
    def move_head_left(self):
        # no decrement for edx
        # may have to add FFFF thing to decrement
        # move edx into eax, decrement eax, move it back
        tempOutput = "0x00088f34" # 0x00088f34 : mov eax, edx; ret
        tempOutput += "0x0007bc64" # 0x0007bc64 : dec eax; ret
        tempOutput += "0x00121c7d" # 0x00121c7d : mov edx, eax ; mov eax, edx ; ret
        return tempOutput
    def move_head_right(self):
        #NOTE: ADDED NOPS TO BALANCE W/ MOVE_HEAD_LEFT BUT COULD BE VERY WRONG
        tempOutput = "0x0002d654" # : inc edx ; ret
        tempOutput += "0x0001a8bf" #nops
        tempOutput += "0x0001a8bf"
        tempOutput += "0x0001a8bf"
        tempOutput += "0x0001a8bf"
        return tempOutput
    def increment_reg(self, reg):
        if(reg == "eax"):
            return "0x000270ea"
        if(reg == "ebp"):
            return "0x00035832"
        if (reg == "ebx"):
            return "0x0002d216"
        if(reg == "edx"):
            return "0x0002d654"
        if(reg == "esi"):
            return "0x000651a6"
        if(reg == "esp"):
            return "0x00020668"  
    def decrement_reg(self, reg):
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
    # EAX = EAX - ECX
    def eax_minus_ecx(self):
        return "0x00150e98"
    # EAX = EAX + ECX
    def eax_plus_ecx(self):
        return "0x00098a40"     
    def zero_out_reg(self, reg):
        if(reg == "eax"):
            return "0x0002ff9f" # xor eax, eax
        if(reg == "esi"):
            tempOutput = ""
            # 0x0006ecc0 : xor esi, esi ; pop ebx ; mov eax, esi ; pop esi ; pop edi ; ret
            # push edi
            tempOutput += self.push_register("edi")
            # push esi
            tempOutput += self.push_register("esi")
            # push ebx
            tempOutput += self.push_register("ebx")
            tempOutput += "0x0006ecc0" # xor esi, esi
            return tempOutput
        if(reg == "ecx"):
            #trashes eax
            tempOutput = ""
            # 0x00116fc3 : xor ecx, ecx ; mov eax, ecx ; pop ebx ; pop esi ; ret
            tempOutput += self.push_register("esi")
            tempOutput += self.push_register("ebx")
            tempOutput += "0x00116fc3" # xor ecx, ecx
            return tempOutput
        if(reg == "ebx"):
            tempOutput = ""
            # 0x000808c2 : xor ebx, ebx ; mov eax, ebx ; pop ebx ; pop esi ; pop edi ; ret
            tempOutput += self.push_register("edi")
            tempOutput += self.push_register("esi")
            tempOutput += self.push_register("ebx") # trash eax
            tempOutput += "0x000808c2" # xor ecx, ecx
            return tempOutput
        # for other registers, no xor command
        # TODO: figure out way to zero out others
    # register value must be 0
    def move_flags_eax(self, reg):
        # NOTE: probably don't need so ignore issues for time being
        # LAHF with RETF 0x0003b5d2 : lahf ; retf // 9fcb
        # TODO: CHECK IF RETF IS OK
        return "0x0003b5d2" # loads flags into EAX
    # used neg instruction: negates a value by finding 2's complement of its single operand
    # NEG AFFECTS FLAGS
    def negate_reg(self, reg): # use negate when we want to use carry flag in jump function
        # XOR it with FFFF?
        if(reg == "eax"):
            return "0x000654b0"
        if(reg == "edx"):
            return "0x0001b0ac"
    def not_reg(self, reg): # use not to go from FFFF to zero value
        return ""
    def push_register(self, reg):
        if(reg == "eax"):
            return "0x0002e745"
        if (reg == "ecx"):
            #0x0008ae23 : push ecx ; add al, 0x5b ; ret // TRASHES EAX
            return "0x0008ae23"
        if(reg == "edi"):
            return "0x000e5705"
        if(reg == "edx"):
            return "0x00158848"
        if(reg == "esi"):
            return "0x000603c5"
        if(reg == "esp"):
            return "0x00137dd6"
        if(reg == "ebx"): # will trash eax; 0x000c78c1 : push ebx ; or al, 0x83 ; ret; OR's al
            return "0x000c78c1"
    def pop_register(self, reg):
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
        if (reg == "ecx"):
            #push eax, 0x000fdcf0 : pop ecx ; pop eax ; ret
            tempOutput = self.push_register("eax")
            tempOutput += "0x000fdcf0"
            return tempOutput
    def and_eax_register(self, reg):
        if(reg == "ecx"):
            return "0x0002d87e"
        if(reg == "edx"):
            return "0x0002df2e" 
    def set_esp(self, reg):
    # TODO: remove quotes above
        return ""
    def move_state_to_ch(self):
        # NOTE: ASSUMES STATE IS ON STACK
        output = self.pop_register("eax")
        output += "0x0006ea87"  # or ch, al ; ret
        return output
    def add_eax_to_edx(self):
        # 0x00121c91 : add edx, eax ; pop ebx ; pop esi ; mov eax, edx ; ret
        tempOutput = self.push_register("esi")
        tempOutput += "0x0012e414" # push random instead of pushing ebx; push 0x1185f89
        tempOutput += "0x00121c91" # add edx, eax
        return tempOutput
    def jump(self):
        #print("in jump")
        # mov eax into temp register (edi)
        output = ""
        output += self.push_register("eax")
        output += self.pop_register("edi")
        # sub eax, ebx
        #0x000994ba : sub eax, ebx ; pop ebx ; pop esi ; ret
        output += self.push_register("esi")
        output += self.push_register("ebx")
        output += "0x00150e98"
        # neg eax
        output += "0x000654b0"
        # add with carry (adc reg, reg)
        output += self.zero_out_reg("esi")
        output += "0x0007773c"
        # push esi, pop eax
        output += self.push_register("esi")
        output += self.pop_register("eax")
        # neg reg
        output += self.negate_reg("eax")
        # mov esp_delta into temp register - edx has esp delta
        #save edx (head) in esi, bc need to use edx for esp_delta
        output += self.push_register("edx")
        output += self.pop_register("esi") # esi has edx value, aka head; edi has eax AKA symbol
        #TODO: PUT ESP_DELTA INTO EDX
        # esp_delta = 74 -> change this
        output += "0x4a"        #TODO:********unsure if this is allowed*************
        output += self.pop_register("edx")
        # and eax, esp_delta
        output += self.and_eax_register("edx") # and eax, edx (esp_delta)
        output += self.increment_reg("ebx")
        # eax has the value that we need, esi has the head value
        # add esp, eax
        # popping esp into a separate reg
        # doing the conditional addition
        # pushing the new esp value back onto the stack
        # popping that value back into esp. 
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
        # NOTE: THIS SECTION IS zeroing out ebx & moving input symbol to AL
        # xchg eax, ebp
        helperOutput += "0x0002d455" # xchg eax, ebp ; ret
        # zero out ecx for counter; NOTE:  WILL TRASH EAX
        helperOutput += self.zero_out_reg("ebx")
        # restore eax using xchg
        helperOutput += "0x0002d455" # xchg eax, ebp ; ret
        #eax now has input symbol again

        #TODO: change code to compare eax (state/symbol) & ebx (counter)
        for i in range(0, length):
            helperOutput += self.jump()
            # restore registers: esi to edx, edi to eax
            helperOutput += "0x00020a3d" # xchg eax, edi ; ret
            helperOutput += self.push_register("esi")
            helperOutput += self.pop_register("edx")
            output = scan.readline()
            #print(output)
            outputArr = output.split(" ")
            helperOutput += self.write_head(outputArr[3])
            # check for accept/reject state. else, call helper again
            #print(outputArr[2])
            if (outputArr[2] == 'r'):
                #print("reject")
                helperOutput += "exit(1)"
                #return helperOutput
            
            elif (outputArr[2] == 'a'):
                #print("accept")
                helperOutput += "exit(0)"
                #return helperOutput
            else:
                helperOutput += self.zero_out_reg("ecx")
                #TODO: ***********unsure if this is allowed*************
                helperOutput += outputArr[2]
                helperOutput += self.move_state_to_ch()
                #at this point, the new state is in ecx, move to eax, al is 0
                helperOutput += self.push_register("ecx")
                helperOutput += self.pop_register("eax")
                #check direction
                if(outputArr[4] == 'R'):
                    helperOutput += self.move_head_right()
                else:
                    helperOutput += self.move_head_left()
                #helperOutput = self.helper(helperOutput, scan, length)
                #return self.helper(helperOutput, scan, length)
        return helperOutput

    def main(self, filename):
        #print("hello")
        # NOTE: will probably have to increment by 2 or 3 instead of 1 for mem location
            # bc we also have to include compare/jump instructions
            # compare sets the flag, JNE checks the flag
        # write input symbols into memory
        # loop from 0-100, 0-255 and every time, 
        # inc mem location and inc temp register
        # move register value to mem location
        # set register back to 0 once you exit inner loop
        output = ""
        output += self.initialize_head_state()
        output += self.zero_out_reg("eax")
        output += self.zero_out_reg("ecx") # no zero out for ecx ATM
        input_ = open(filename, 'r')
        inputLines = input_.readlines()
        length = len(inputLines)
        input_.close()
        scan = open(filename, 'r')
        print(self.helper(output, scan, length))
a = ROP()
a.main("testing.txt")


            
            

