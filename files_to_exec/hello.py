import sys

print("hello stdout")
print("hello stderr", file=sys.stderr)

# Force an error by dividing by zero
result = 1 / 0