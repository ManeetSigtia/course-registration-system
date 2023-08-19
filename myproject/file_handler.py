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
    file_path = r'files/final.dat'
    with open(file_path, 'wb') as binary_file:
        pickle.dump(contents, binary_file)


# function to read contents of file
def binary_file_reader():
    file_path = r'files/final.dat'
    with open(file_path, 'rb') as binary_file:
        contents = pickle.load(binary_file)
        return contents


# function to write reports in text files
def text_file_writer(contents, name):
    file_name = r'files/print_%s.txt' % name
    with open(file_name, 'w') as text_file:
        text_file.write(contents)
