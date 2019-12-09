# Computes the gcd of two numbers a and b
# Result in r0
movi r0, 40     # a
movi r1, 45     # b
movi r10, 0
movi r2, 0      # i = 0     --- Beginning of loop 1
addi r2, 1      # i = i + 1 --- Beginning of loop 2
mov r3, r1      # b copy
mul r3, r2      # b * i
cmp r0, r3      # branch if b*i < a <-> a > b*i
bg 7            #           --- End of loop 2
be 14           # If a = b*i i.e r0 = r3, no need to execute the next instruction
sub r3, r1      # b * i such that a > b*i but a < b*(i+1)
mov r2, r0      # a copy
sub r2, r3      # a - b*i = r
mov r0, r1      # a = b
mov r1, r2      # b = r = a - b*i
cmp r1, r10     # if b>0, go back to loop 1
bg 6            #           --- End of loop 1
hlt