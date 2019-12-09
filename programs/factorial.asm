movi r0, 6      # Fact(6)
br 4
hlt
movi r1, 1      # --- Start of function definition
cmp r0, r1
bg 9            # Branch if r0 > 1
movi r0, 1      # r0 <= 1 so fact(1) = fact(0) = 1
ret             # End
push r0
subi r0, 1      # n-1
br 4            # Call routine: returns fact(n-1)
pop r1          # Get n back
mul r0, r1      # n*fact(n-1)
ret             # --- End of function definition
hlt