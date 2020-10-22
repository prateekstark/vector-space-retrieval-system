# Vector Space Retrieval System
This an end-to-end retrieval system for English to perform a toy-scale performance evaluation of Vector-space retrieval models.

## Installation

The following command will install all the dependencies:

```bash
./build.sh
```

## Usage
For constructing the index:
```bash
python invidx_cons.py path/to/colection/folder index_filename #Example: python invidx_cons.py data/TaggedTrainingAP/ indexfile
```

For searching the index for the queries:
```bash
python vecsearch.py --query queryfile --cutoff k --output resultfile --index indexfile --dict dictfile
#Example: python vecsearch.py --cutoff 10 --query data/topics.51-100 --output resultfile --dict indexfile.dict --index indexfile.idx
```

For printing the index file dictionary:
```bash
python printdict.py path/to/dict #Example: python printdict.py indexfile.dict
```
## Algorithmic Detail
This is a basic implementation of the VSM. Firstly, the input documents are parsed and two indexfiles are created (indexfile.idx and indexfile.dict). These files take much less space than the original documents (around 1/4th) and help in faster searching.

After this while running the search component, initially, all the queries are parsed and considered as independent documents. Then we find the similarity of each query with all the "possible documents", rank them in decreasing order of similarity, and write them to the result file for final trec_eval evaluation.

#### Preprcessing Detail:
For preprocessing, first, the stopwords are removed, the text is tokenized and finally stemmed with SnowballStemmer (nltk).

#### Pseudo Code:
```
FUN find_score(doc1, doc2):
    represent doc1 and doc2 as vectors of terms with their respective count as the magnitude
    score = dot product between two documents
    normalized_score = score / normalization_factor 
    # here the normalization factor is a heuristic is taken to be the product of magnitude of doc1_vector and doc2_vector
    return normalized_score

FUN fetch_possible_document(query):
    possible_documents = {}
    for doc in all_docs:
        if any term of query present in doc:
            add doc to possible_documents
    return possible documents
  
FUN search(query, cutoff):
    ranklist = {}
    possible_documents = fetch_possible_documents(query)
    for doc in possible_documents:
        score = find_score(query, doc) #Cosine Similarity
        add score to ranklist
    sort(ranklist)

    return top k(=cutoff) elements of ranklist
```
Note: The two functions fetch_possible_document and search might seem similar and redundant but they are made for making the implementation faster. Please let me know if you have some suggestion for this.

## Results
For the given data, the indexing time is around 500 seconds while nDCG@10 = 0.27 and F_set@100 = 0.11.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.