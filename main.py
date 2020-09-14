# print("Hello IT!")

import urllib.request as urlrequest
import urllib.parse as urlparser
import os
import shutil
import ntpath
import re

DOWNLOAD_FOLDER_PATH = './downloads/'
TARGET_FOLDER_PATH = DOWNLOAD_FOLDER_PATH + 'content/'
FILE_NAME_PATTERN = '(?<=href=").+\.pdf(?=")'

# Simple lib test
print('Downloading with urllib3...')
urlrequest.urlretrieve('https://www.google.com', DOWNLOAD_FOLDER_PATH + 'google_welcome.html')
print('... Done!')

# trying a PDF file
print('Downloading a PDF sample...')
urlrequest.urlretrieve('https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch4-7sep.pdf', DOWNLOAD_FOLDER_PATH + 'sample_pdf.pdf')
print('...Done!')


################################ Stop playing #########################################

# Cleaning and recreating landing folder
print('Cleansing local storage...')
if os.path.exists(TARGET_FOLDER_PATH):
    shutil.rmtree(TARGET_FOLDER_PATH)

os.makedirs(TARGET_FOLDER_PATH)
print('...Done!')


# Retrieving the entry point
MAIN_PAGE_URL = 'https://www.cl.cam.ac.uk/~rja14/book.html'

print('Downloading the main page...')
index_file_path = TARGET_FOLDER_PATH + 'index.html'
urlrequest.urlretrieve(MAIN_PAGE_URL, index_file_path)
print('...Done!')

# CAUTION: the file names broken up on several lines will failed to be caught!
regex = re.compile(FILE_NAME_PATTERN)
# main_page_base_url = urlparser.urlsplit(MAIN_PAGE_URL).netloc  # E.g.: www.cni.nl:80
id = 0

with open(index_file_path, 'r') as index:
    for line in index:
        matches = regex.findall(line)

        if matches:
            for match in matches:
                # https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse
                resource_url = urlparser.urljoin(MAIN_PAGE_URL, match)
                resource_basename = ntpath.basename(match)
                print(str(id) + ': ' + resource_basename + ' --> ' + resource_url + ' ... ', end='')
                # CAUTION: assuming <= 1k files to retrieve
                urlrequest.urlretrieve(resource_url, TARGET_FOLDER_PATH
                                       + 'DWL_' + str(id).rjust(3, '0') + '__' + resource_basename)
                print('OK!')

                id += 1



