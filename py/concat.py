def writeout(path,out):
	with open(path) as file:
		f.readlines()
	for line in f[1:]:
		out.write(line)

if len(sys.argv) < 2:
		print('Usage:', str(sys.argv))
		print('\t','python concat.py <csv1...n>')
		print('Assumes CSVs of the same shape + headers, vertical concatenation.\n', str(sys.argv))
else:
	# timestamp for a unique filename
	timestamp = int(time.time())
	# make a new unique directory for CSVs to live in
	directory = "concatenated_csv" + "_" + str(timestamp)
	if not os.path.exists(directory):
		os.makedirs(directory)	

	with open(sys.argv[1]) as file:
		csv = file.readlines()

	concat = open(directory + '/' + 'concat' + '_' + timestamp)
	concat.write(csv[0]) # header

	for path in sys.argv[1:]:
		writeout(path,concat)