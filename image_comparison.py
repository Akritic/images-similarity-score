import os
from find_similarity_helper import find_similarity
import csv
import sys
import time
from datetime import datetime


DEFAULT_REJECT_FILE = "Comparison_Rejection_"
DEFAULT_FILE_PREFIX = 'Comparison_Results_'
SUPPORTED_FILE_EXTENSION = set(['.PNG', '.JPG', '.GIF'])
HEADERS = 'image1, image2, similar, elapsed \n'



def write_to_file(image1, image2, similar_score, elapsed_time, output_file):
    output_string = image1 + ',' + image2 + ',' + similar_score + ',' + elapsed_time + '\n'
    output_file.write(output_string)


def is_input_valid(image_1, image_2, reject_file):
    result = True
    rejection_reason = ""
    if not os.path.exists(image_1) or not os.path.exists(image_2):
        rejection_reason += "Input image does not exists on specified path. "
        result = False

    file_one_Name, file_one_extention = os.path.splitext(image_1)
    file_two_Name, file_two_extention = os.path.splitext(image_2)

    if file_one_extention.upper() not in SUPPORTED_FILE_EXTENSION or file_two_extention.upper() not in SUPPORTED_FILE_EXTENSION:
        result = False
        rejection_reason += "File extension is not supported."

    if not result:
        rejected_line = image_1 + ',' + image_2 + ',' + rejection_reason + '\n'
        reject_file.write(rejected_line)

    return result


def compare_images(input_file=None):
    if input_file is None:
        input_file = input("Please enter the input file with absoulute path: ")

    if not os.path.exists(input_file):
        print("File does not exist, please try again with correct path")
        return

    read_file = open(input_file)
    csv_reader = csv.reader(read_file)
    next(csv_reader)

    output_file_name = DEFAULT_FILE_PREFIX + datetime.now().strftime("%Y%m%d_%H%M%S%f") + '.csv'
    output_file = open(output_file_name, 'w')
    output_file.write(HEADERS)
    reject_file_name = DEFAULT_REJECT_FILE + datetime.now().strftime("%Y%m%d_%H%M%S%f") + '.csv'
    reject_file = open(reject_file_name, 'w')

    for row in csv_reader:

        # File is not valid, skipping the record
        if not is_input_valid(row[0], row[1], reject_file):
            continue

        start_time = time.time()
        similarity_score = find_similarity(row[0], row[1])
        elapsed_time = "%.3f" % (time.time() - start_time)

        write_to_file(row[0], row[1], similarity_score, elapsed_time, output_file)

    output_file.close()
    reject_file.close()
    read_file.close()
    print("Results will be stored in file : {}".format(output_file_name))
    print("Rejected results stored in file : {}".format(reject_file_name))


if __name__ == '__main__':

    if len(sys.argv) >1 and sys.argv[1] == 'test':
        compare_images('tests/test_input.csv')
    else:
        compare_images()
