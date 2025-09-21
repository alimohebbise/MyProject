from collections import deque

# create an empty queue
queue = deque()

# enqueue (add) elements
queue.append(10)
queue.append(20)
queue.append(30)

print("Queue after enqueues:", queue)

# dequeue (remove) elements
x = queue.popleft()
print("Dequeued element:", x)
print("Queue after dequeue:", queue)

y = queue.popleft()
print("Dequeued element:", y)
print("Final queue:", queue)
