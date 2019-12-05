# Branch tests
# Test if not equal
movi r0, 10 # r0 = 10
movi r1, 1  # r1 = 1
cmp r0, r1  # r0 != r1
be 25       # Not taken. If taken, exit code r0 = 10

# Test greater than
movi r0, -1  # r0 = -1
cmp r1, r0  # r1 > r0
bg 15       # Branch taken: jump over the NOP
b 25        # Else exit code r0 = -1

# Test not greater than
movi r0, 5 # r0 = 5
cmp r1, r0  # r1 < r0
bg 25       # Not taken. If taken, exit code r0 = 5

movi r0, 0  # r0 = 0
movi r1, 0  # r1 = 0
cmp r0, r1  # r0 = r1
be 25       # Taken with successful exit code r0 = 0
movi r0, 1  # Else exit code r0 = 1

hlt