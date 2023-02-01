import pickle

# in the 2D array:
# course names corresponds to array[0]
# age groups corresponds to array[1]
# course objects correspond to array[2]
# schedule objects correspond to array[3]
# student objects correspond to array[4]
# registration objects correspond to array[5]
# term objects correspond to array[6]
# users correspond to array[7]


# funtion to save objects in file
def binary_file_writer(contents):
    binary_written_file = open(r'final.dat', 'wb')
    pickle.dump(contents, binary_written_file)
    binary_written_file.close()


# function to read contents of file
def binary_file_reader():
    binary_read_file = open(r'final.dat', 'rb')
    contents = pickle.load(binary_read_file)
    binary_read_file.close()
    return contents


# function to write reports in text files
def text_file_writer(contents, name):
    file_name = r'print_%s.txt' % name
    text_read_file = open(file_name, 'w')
    text_read_file.write(contents)
    text_read_file.close()
