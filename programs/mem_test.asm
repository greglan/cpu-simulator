movi r0, 0      # First vector
movi r1, 0
movi r2, 256
str r0, r1      # *addr = r0
addi r0, 1      # r0++
addi r1, 1      # addr++
cmp r2, r1
bg 4
movi r0, 255    # Second vector
movi r1, 256
movi r2, 512
str r0, r1      # *addr = r0
subi r0, 1      # r0--
addi r1, 1      # addr++
cmp r2, r1
bg 12
movi r0, 0      # src1 -- Compute the sum
movi r1, 256    # src2
movi r2, 255    # Length
movi r3, 0      # Sum s
movi r4, 0      # Counter
ldr r11, r0, r4 # val1
ldr r12, r1, r4 # val2
add r11, r12    # val1 + val2
add r3, r11     # s = s + val1 + val2
addi r4, 1      # i++
cmp r2, r4
bg 22          # 255 * 255 = 0xfe01
hlt