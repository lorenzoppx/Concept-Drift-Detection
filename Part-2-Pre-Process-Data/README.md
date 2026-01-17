# Part-2-Pre-Process-Data

This part is for pre process the data of social networks with filtering purposes and generate embeddings. 

## Filter for too close posts (spacy)

Using the embeddings of spacy for each text of the document and put a limiar of threshold distance for filter too close posts. The threshold is put per default 0.92.

```
python filter_spacy.py
```

## Generate embeddings using spacy

Generate embeddings of spacy for each text of the document and add a column to origin .csv files.

```
python generate_embedding_spacy.py
```
## Convert .csv to .hdf5 format

Convert .csv files to .hdf5. This conversion is used for better for a large amount of rows. For visualize the HDF5 files easily [here](https://myhdf5.hdfgroup.org/).

```
python csvtohdf5.py
```

## Metrics counts of 2 days window without and with overlapping

For see this window of 2 days count without and with overlapping.

```
python metric_count_per_day.py
```