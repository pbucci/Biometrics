import sys

def nth(n):
	if n == 1:
		return "1st"
	if n == 2:
		return "2nd"
	if n == 3:
		return "3rd"
	return str(n) + "th"

def fib(i,j,n):
	if n == 0:
		return i
	k = i + j
	m = n - 1
	return fib(j,k,m)

if len(sys.argv) < 2:
		print('Usage:', str(sys.argv))
		print('\t','python fib.py <n>')
else:
	n = int(sys.argv[1])
	print("The " + nth(n) + " fibonacci number is: " + str(fib(0,1,n-1)))
