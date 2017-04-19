
patch_file = "mapping/mapped.csv"

with open(patch_file, "r") as pfile:
	print(pfile.readline())
	for patch in pfile:
		(board_idx, data_idx) = patch.strip().split(",")
		patch_str = "patched[{}] = data[{}]".format(str(board_idx), str(data_idx))
		print(patch_str)
