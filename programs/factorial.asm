# Computes the factorial of a number
movi r0, 6      # Fact(6)
br 7
b 21

# Function definition
movi r1, 1
cmp r0, r1

bg 14           # Branch if r0 > 1
movi r0, 1      # r0 <= 1 so fact(1) = fact(0) = 1
b 19            # End

push r0
subi r0, 1      # n-1
br 6            # Call routine: returns fact(n-1)
pop r1          # Get n back
mul r0, r1      # n*fact(n-1)
ret

hlt