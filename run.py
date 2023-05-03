import requests
import os
import urllib3
import threading
import time

urllib3.disable_warnings()

count = 0
# Define the URL prefix and folder to save the PDFs
url_prefix = "https://ceo.karnataka.gov.in/Elections_rolls_2023/KANNADA/MR/"
pdf_folder = "pdfs_multi/"

# Create the folder if it does not exist
if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

# Define a function to download a PDF file
def download_pdf(url, filename):
    # print("Downlaod url is " , url , "and filename is " , filename)
    full_url = url
    response = requests.get(full_url, verify=False)
    if response.status_code == 200:
        with open(os.path.join(pdf_folder, filename), "wb") as pdf_file:
            pdf_file.write(response.content)
            global count
            count += 1
            print( f"File No downloaded {count}/59703 succcesful")
    else:
        print("Download failed in download_pdf function and status code is ", response.status_code)

# Open the text file containing the links
with open("all_pdf_links.txt", "r") as f:
    # Create a list of URLs and filenames to download
    urls_and_filenames = [(line.strip(), line.strip().split("/")[-1]) for line in f]

# Define the number of threads to use
num_threads = 18


# Create a list of threads to download the PDF files
threads = []
for i in range(num_threads):
    threads.append(threading.Thread())

# Start the threads
for i in range(num_threads):
    thread_urls_and_filenames = urls_and_filenames[i::num_threads]
    threads[i] = threading.Thread(target=lambda urls_and_filenames: [download_pdf(url, filename) for url, filename in urls_and_filenames], args=[thread_urls_and_filenames])
    threads[i].start()

# Wait for all threads to finish
for i in range(num_threads):
    threads[i].join()

print("All PDF files downloaded.")