# Branch tests
movi r0, 10 # r0 = 10
movi r1, 1  # r1 = 1
cmp r0, r1  # r0 != r1
be 7        # Not taken

movi r0, 0  # r0 = 0
cmp r1, r0  # r1 > r0
bg 12       # Branch taken: jump over the NOP

and r0, r0  # NOP
movi r0, 10 # r0 = 10
cmp r1, r0  # r1 < r0
bg 20       # Not taken

movi r0, 0  # r0 = 0
movi r1, 0  # r1 = 0
cmp r0, r1  # r0 = r1
be 21

movi r1, 0  # r1 = 1
movi r1, 1  # r1 = 1
