def save_to_file(file_name, txt):
    file = open(str(file_name) + '.txt', 'w')
    file.write(txt)
    file.close()

def read_file(file_name):
    file = open(str(file_name) + '.txt', 'r')
    read = file.read()
    file.close()
    return read
