# Computes the gcd of two numbers a and b
# Result in r0
movi r0, 45     # a
movi r1, 40     # b
movi r10, 0

movi r2, 0      # i = 0, beginning of loop 1
add r2, r2, 1   # i = i + 1, beginning of loop 2
mov r3, r1      # b copy
mul r3, r2      # b * i
cmp r0, r3      # a - b*i
bg 7            # end of loop 2
sub r3, r1      # b * i such that a > b*i but a < b*(i+1)
mov r0, r1      # a = b
sub r1, r3      # b = a - b*i
cmp r1, r10     # if b>0, go back to loop 1
bg 6

hlt