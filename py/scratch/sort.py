import sys

# slow reverse insertion sort
def sort(orig,s):
	n = max(orig)
	out = orig.remove(n)
	s.append(n)
	if out == None:
		return s
	return sort(out,s)

if len(sys.argv) < 2:
		print('Usage:', str(sys.argv))
		print('\t','python sort.py <n>')
else:
	n = int(sys.argv[1])
	x = [x for x in range(0,n)]
	sort(x,[])
	
	print("Sorted x")
