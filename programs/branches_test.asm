movi r0, 10 # r0 = 10 --- Test if not equal
movi r1, 1  # r1 = 1
cmp r0, r1  # r0 != r1
be 17       # Not taken. If taken, exit code r0 = 10
movi r0, -1 # r0 = -1 --- Test greater than
cmp r1, r0  # r1 > r0
bg 9        # Branch taken: jump over the NOP
b 17        # Else exit code r0 = -1
movi r0, 5  # r0 = 5. --- Test not greater than
cmp r1, r0  # r1 < r0
bg 17       # Not taken. If taken, exit code r0 = 5
movi r0, 0  # r0 = 0
movi r1, 0  # r1 = 0
cmp r0, r1  # r0 = r1
be 17       # Taken with successful exit code r0 = 0
movi r0, 1  # Else exit code r0 = 1
hlt