from InvertedIndex import InvertedIndex
from bs4 import BeautifulSoup
import argparse
import random

"""
To Do:
	1) Parse Args
	2) Parse queryfile to read and generate file finally
	3) Match all the submission instructions
	4) Search for better saving and loading techniques
	5) Run of full fledged dataset --done
	6) Make a priority queue data structure, to reduce the ranking time
	7) Think about evaluation strategy
"""


def get_query_list(queryfile_path):
    file = open(queryfile_path)
    content = file.readlines()
    file.close()
    content = "".join(content)
    bs_content = BeautifulSoup(content, "lxml")
    queryList = []
    queryMap = {}
    for query_doc in bs_content.find_all("num"):
        qid = query_doc.get_text().partition("\n")[0].strip()[8:].strip()
        query = query_doc.title.get_text().partition("\n")[0].strip()[7:].strip()
        queryList.append(query)
        queryMap[query] = qid
    return queryList, queryMap


def write_resultfile(filename, ranklist, queryIdMap):
    file = open(filename, "w")
    for query in ranklist:
        rank = 1
        for doc_id in ranklist[query]:
            file.write(
                "{} {} {} {} {} {}\n".format(
                    queryIdMap[query].lstrip("Q0"),
                    0,
                    doc_id[0],
                    rank,
                    doc_id[1],
                    "STANDARD",
                )
            )
            rank += 1
    file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=10)
    parser.add_argument("--query", type=str, default="data/topics.51-100")
    parser.add_argument("--index", type=str, default="./indexfile.idx")
    parser.add_argument("--dict", type=str, default="./indexfile.dict")
    parser.add_argument("--output", type=str, default="resultfile")
    args = parser.parse_args()

    invidx = InvertedIndex(
        dictionary_filepath=args.dict, postings_list_filepath=args.index
    )
    queryfile = args.query
    queryList, queryIdMap = get_query_list(queryfile)

    ranklist = {}
    for query in queryList:
        ranklist[query] = invidx.get_ranking_list(query)[: args.cutoff]

    write_resultfile(args.output, ranklist, queryIdMap)
    del invidx
    del ranklist
