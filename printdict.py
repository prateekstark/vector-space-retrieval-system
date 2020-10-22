from utils import load_file
import sys


if __name__ == "__main__":
    dictionary_filepath = "indexfile.dict"
    if len(sys.argv) == 3:
        dictionary_filepath = sys.argv[2]
    dictionary = load_file(dictionary_filepath)

    for category in ["organization", "person", "location", "rest"]:
        for word in dictionary[category]:
            if category == "person":
                print(
                    "p:{} {} {}".format(
                        word,
                        dictionary[category][word][0],
                        dictionary[category][word][1],
                    )
                )
            elif category == "organization":
                print(
                    "o:{} {} {}".format(
                        word,
                        dictionary[category][word][0],
                        dictionary[category][word][1],
                    )
                )
            elif category == "location":
                print(
                    "l:{} {} {}".format(
                        word,
                        dictionary[category][word][0],
                        dictionary[category][word][1],
                    )
                )
            else:
                print(
                    "{} {} {}".format(
                        word,
                        dictionary[category][word][0],
                        dictionary[category][word][1],
                    )
                )
    del dictionary
