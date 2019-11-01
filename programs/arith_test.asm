movi r0, 1000   # r0 = 1000
movi r1, 1
mov r2, r1  # r2 = 1
movi r3, 3
movi r4, 4  # r4 = 4
movi r5, 5  # r5 = 5
movi r6, 6  # r6 = 6

sub r1, r0  # r1 = -999
add r1, r0  # r1 = 1
add r2, r1  # r2 = 2
mul r2, r0  # r2 = 2*1000 = 2000 = 0x7d0
div r6, r3  # r6 = 2

and r3, r1  # r3 = 0b11 & 0b01 = 1
xor r0, r0  # r0 = 0
not r7, r6  # r7 = ~0b10 = 2^32-1-2 ?
or r8, r6   # r8 = r8 || r6 = r6 = 0x2

movi r9, 4
mov r10, r9
movi r11, 2
lsl r9, r11     # r9 = 4 << 2 = 16 = 0x10
lsr r10, r11    # r10 = 4 >> 2 = 1