# create an empty stack
stack = []

# push elements onto the stack
stack.append(10)
stack.append(20)
stack.append(30)

print("Stack after pushes:", stack)

# pop elements from the stack
x = stack.pop()
print("Popped element:", x)
print("Stack after pop:", stack)

y = stack.pop()
print("Popped element:", y)
print("Final stack:", stack)
