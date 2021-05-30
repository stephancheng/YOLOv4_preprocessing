import glob, os

# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

print(current_dir)

current_dir = 'data/test_images'

file_test = open('data/final_test.txt', 'w')

for pathAndFilename in glob.iglob(os.path.join(current_dir, "*.jpg")):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    file_test.write("data/test_images" + "/" + title + '.jpg' + "\n")
