# Store two 256 bytes vector in memory and compute the sum
# First vector: increasing values from 0 to 255
movi r0, 0
movi r1, 0
movi r2, 256
str r0, r1      # *addr = r0
addi r0, 1     # r0++
addi r1, 1     # addr++
cmp r2, r1
bg 6

# Second vector: all 1s
movi r0, 1
movi r1, 256
movi r2, 512
str r0, r1      # *addr = r0
addi r1, 1     # addr++
cmp r2, r1
bg 16

# Compute the product
movi r0, 0      # src1
movi r1, 256    # src2 and length
movi r2, 0      # Index
movi r3, 0      # Result
ldr r11, r0, r2 # val1
ldr r12, r1, r2 # val2
mul r11, r12    # val1 + val2
add r3, r11     # s = s + val1 + val2
addi r2, 1      # index++
cmp r1, r2
bg 26          # sum([k for k in range(256)]) = 0x7f80

hlt