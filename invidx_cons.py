import os
import sys
import time
from bs4 import BeautifulSoup
from InvertedIndex import InvertedIndex


if __name__ == "__main__":
    """
    Default Values of folder path and index-filename
    """
    path = "/home/stark/Projects/vector-space-retrieval-system/data/sample/"
    index_filename = "indexfile"

    if len(sys.argv) == 3:
        path = sys.argv[1]
        index_filename = sys.argv[2]
    start_time = time.time()
    idx = InvertedIndex()
    for filename in os.listdir(path):
        print(filename)
        file = open(path + filename)
        content = "".join(file.readlines())
        file.close()
        bs_content = BeautifulSoup(content, "html.parser")
        for doc in bs_content.find_all('doc'):
            idx.add_doc(doc)
    
    idx.assign_postings_list()
    idx.save()
    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))
    del idx