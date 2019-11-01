# Store two 256 bytes vector in memory and compute the sum
# First vector
movi r0, 0
movi r1, 0
movi r2, 256
str r0, r1      # *addr = r0
addi r0, 1     # r0++
addi r1, 1     # addr++
cmp r2, r1
bg 6

# Second vector
movi r0, 255
movi r1, 256
movi r2, 512
str r0, r1      # *addr = r0
subi r0, 1     # r0--
addi r1, 1     # addr++
cmp r2, r1
bg 16

# Compute the sum
movi r0, 0      # src1
movi r1, 256    # src2
movi r2, 255    # Length
movi r3, 0      # Sum s
ldr r11, r0     # val1
ldr r12, r1     # val2
add r11, r12    # val1 + val2
add r3, r11     # s = s + val1 + val2
addi r0, 1      # src1++
addi r1, 1      # src2++
cmp r2, r0
bg 27          # 255 * 255 = 0xfe01