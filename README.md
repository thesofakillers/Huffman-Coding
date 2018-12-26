# Huffman Coding

Originally made for Durham University's Department of Computer Science's course _Software Methodologies_ under the sub-module _Digital Communications_, as part of the coursework in 2017/2018.

This repository contains an implementation of [Huffman Coding](https://en.wikipedia.org/wiki/Huffman_coding) for .txt files.

I have included the .txt files I have tested my implementation on in the same directory for ease of use, since the script and the files you wish to encode are to be in the same directory for it to work smoothly.

## Requirements

This project was made utilizing [Python 3.6](https://www.python.org/downloads/release/python-360/) and should work with all 3.X versions.

In addition, please ensure that the following modules are installed:

-   [bitstring](https://pypi.org/project/bitstring/)
-   [NumPy](http://www.numpy.org/)

## Instructions

### Encoding

To encode a file, please:

1.  Open a console window and navigate to a directory containing huffman.py and the plain text document file you wish to encode using the cd command
2.  type `python huffman.py e filename.txt` where `filename.txt` is to be re-
    placed by the name of the file you wish to encode.

A file `filename.hc` should appear in the same directory, ready for decoding

### Decoding

To decode a file, please:

1.  Open a console window and navigate to a directory containing huffman.py and the .hc file you wish to decode located using the cd command. Ensure that the .hc file was in fact created by huffman.py and not some other script.
2.  type `python huffman.py d filename.hc` where `filename.hc` is to be replaced by
    the name of the file you wish to encode.

A file `filename decoded.txt` should appear in the directory.
