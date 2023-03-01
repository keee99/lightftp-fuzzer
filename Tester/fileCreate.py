import os
import random
import string

# Define the directory to create the files in
dir_path = os.getcwd()+'/seeds'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
# adjust path and create a fuzzing file folder to store all the files

# Define the number of files to create
num_files = 200

# Define the length of the random filename
# Define the range of possible filename lengths
min_length = 1
max_length = 23

# Define the set of characters to use in the filename
filename_chars = string.ascii_letters + string.digits + string.punctuation

def main():
# Create the specified number of files
    for i in range(num_files):
        # Generate a random filename length
        filename_length = random.randint(min_length, max_length)

        # Generate a random filename
        filename = ''.join(random.choice(filename_chars) for i in range(filename_length))

        # Create the file with the random filename
        try:
            with open(os.path.join(dir_path, filename + '.txt'), 'w') as f:
                f.write('This is a random text file.')
                f.close()
            with open(os.path.join(dir_path, 'all_filename.txt'), 'a') as fa: # txt file stores all the writable filenames
                fa.write(filename + "\n")
                fa.close()
                # print("file " + str(i) + "is printed")
        except FileNotFoundError: # Exception error where the file cannot be created
            next
        except OSError: # Exception error where the file cannot be written into
            next

        
if __name__ == '__main__':
    main()