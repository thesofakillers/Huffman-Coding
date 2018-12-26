"""into terminal, type python huffman.py cmd target", where
"cmd" is to be replaced with "e" if encoding or "d" if decoding
and "target" is to be replaced with the name of the file
you wish to encode or decode"""

import sys
import collections
import os
import pickle
import heapq
from bitstring import BitArray, BitStream
import numpy

class Node():
    """
    -A Node of the Huffman binary tree.
    -Nodes have a frequency, value, left and right properties.
    -Value, which corresponds to the character stored in the node, will always
    be None unless the node is a leaf
    -If the node is a leaf, frequency stores the frequency of appearance of the
    specific character. Otherwise, frequency will be the sum of the frequency of
    the node's children
    -left and right correspond to the left and right children nodes
    """

    def __init__(self, frequency, value, left, right):
        self.frequency = frequency #frequency of value
        self.value = value #character
        self.left = left #left Child
        self.right = right #right Child

    def __lt__(self, other): #allows heapq to sort the heap by frequency
        return self.frequency < other.frequency

#parameters that will be passed to the various functions. Defined in terminal
CMD = sys.argv[1] #e to encode, d to decode
TARGET = sys.argv[2] #specifies target file, including extension


"""
input: string specifying name of file to be read
reads file
output: string of contents of file. If "d", also reads the key
"""
def readFile(filename, command):
    if command == "e":
        f = open(filename, "r", encoding = "utf8", newline = '') #opens file for reading
        readString = f.read() #reads the entire file and stores it as a string
        f.close() #closes file now that reading is done
        return readString #return the string that was read
    elif command == "d": #reccomend reading the encoding part of writeFile first
        f = open(filename, "rb") #opens file for reading
        rootNode = pickle.load(f) #deserializes the root node
        comprCode = pickle.load(f) #deserializes the compr message
        paddingParam = pickle.load(f) #deserializes padding parameter
        f.close() #closes file now that reading is done
        encodedMessage = decompress(comprCode, paddingParam) #obtaining string
        return rootNode, encodedMessage # which will be used by decode func
    else:
        print("command not understood, please either type \
'e' when encoding or 'd' when decoding")


"""
input: objects to be written, name of to be written to, command specifying if
encoding or decoding
output: a .hc file if encoding, original file if decoding
"""
def writeFile(source, filename, command):
    if command == "e":
        encFileName = os.path.splitext(os.path.basename(filename))[0]
        #getting original file name without .txt extension
        f = open(encFileName + ".hc", "wb") #creating file to write to
        pickle.dump(source[0], f) #serializing the root node to the file
        comprCode, paddingParam = compress(source[1]) #compressing string
        pickle.dump(comprCode, f) #serializing compressed coded txt to the file
        pickle.dump(paddingParam, f) #serializing the paddingParam
        f.close() #closing the written file
    elif command == "d":
        decFileName = os.path.splitext(os.path.basename(filename))[0]
        #getting original file name without .hc extension
        f = open( decFileName + "_decoded.txt", "w", encoding = "utf8", \
        newline = '') #creating file to write to
        f.write(source) #writing decoded text
        f.close() #closing the written file
    else:
        print("command not understood, please either type \
'e' when encoding or 'd' when decoding")


'''
input: string
output: list of ordered pairs of (character, frequency), sorted by frequency
'''
def freq_order(string):
    return collections.Counter(string).most_common()


"""
input: string of contents of file
function: encodes the contents of the file
output: string of 1s and 0s encoding the file + key for decoding
"""
def encode(inpt):
    frequent_chars = freq_order(inpt)
    #creeating the sorted 2D list of characters and respective frequency

    #initializing list of nodes, to be later made into a heap through heapify
    heap = []
    for i in range(len(frequent_chars)):
    #for each element in the list, place its frequency and value in a Node,
    #and then append that node to the heap
        value, frequency = frequent_chars[i]
        heap.append(Node(frequency, value, None, None))

    heapq.heapify(heap)
    #acttually makes a heap out of the list, taking care it is sorted

    #Associates the nodes with eachother, until only the root is left
    while len(heap) > 1:
        leftChild = heapq.heappop(heap)
        rightChild = heapq.heappop(heap)
        parent = Node(leftChild.frequency+rightChild.frequency, None, leftChild,\
        rightChild)
        heapq.heappush(heap, parent)
        #2 nodes are lost and 1 node is gained for each loop, so the loop will
        #eventually end

    chars_codes = {} #init empty dict to be filled by traversing tree
    traverse(heap[0], "", chars_codes) #traverses tree, fiilling out passed dict
    encodedOutput = "" #init empty string to be filled with encoded input
    for char in inpt: #encodes input by using dict
        encodedOutput += chars_codes[char]

    return heap[0], encodedOutput #returns the root node of tree and encodedStr


"""
inputs: A root node, en empty string, an empty dictionary
Traverses the Huffman tree recursively, encoding its path from a Node until it
reaches a Node with no children, at which point it stores the current Node
value and the respective path to it in the dictionary passed as a parameter.
outputs: explicitly none, although the empty dictionary passed into the function
will result filled by the end of execution.
"""
def traverse(nodeRoot, emptyString, emptyDict):
    if nodeRoot.left != None:
        traverse(nodeRoot.left, emptyString + "0", emptyDict)
    if nodeRoot.right != None:
        traverse(nodeRoot.right, emptyString + "1", emptyDict)
    if (nodeRoot.left == None) and (nodeRoot.right == None):# \
        emptyDict[nodeRoot.value] = emptyString


"""
input: string of 1s and 0s + rootNode
decodes the file by starting at the rootNode and visiting either the left
or right child depending on whether the current bit is a 0 or a 1 respectively.
If the currentNode is a leaf, method writes its value as the decoded path.
output: string of contents of original file
"""
def decode(rootNode, ones_zeros):
    decodedString = "" # initializing empty string
    currNode = rootNode # initializing current Node as root

    for bit in ones_zeros: # looping encoded string bit by bit
        if currNode.left == None and currNode.right == None:
        #if the current Node is a leaf, then add its value to the decoded string
            decodedString += currNode.value
            currNode = rootNode #restart the process from the root Node.
        if bit == "0": #visit left child if bit is 0
            currNode = currNode.left
        else: #visit right child otherwise, i.e. if bit is 1
            currNode = currNode.right

    return decodedString


"""
input: string of 1s and 0s
Converts the characters of the string into actual bits.
output: bytes file representing input, integer Padding Parameter - necessary
for determining how many zeros to add to the string to render it 'byteable'
"""
def compress(ones_zeros):
    toMultiple8 = len(ones_zeros) % 8 #determining Padding Param
    if toMultiple8 != 0:
        ones_zeros = ((8-toMultiple8) * "0") + ones_zeros
                    #^^rendering the string length a multiple of 8
    ones_zeros = BitArray(numpy.fromstring(ones_zeros, numpy.int8) - 48 ).bytes
    #In order: string --> numpy array ---> BitArray ---> bytes object
    return ones_zeros, toMultiple8


"""
input: a bytes file, integer padding parameter outputted by compress func
Converts the bytes file back into a string of ones and zeros, and then gets
rid of the extra 0s added to the start previously to obtain 'byteability'
output: string of 1s and 0s
"""
def decompress(bytesFile, padding):
    ones_zeros = BitArray(bytesFile).bin[8-padding:]
    #converts byte file to bit array, then to binary string, padding then removed
    return ones_zeros


#this part executes the code.
if CMD == "e":
    INPUT = readFile(TARGET, CMD)
    OUTPUT = encode(INPUT)
    writeFile(OUTPUT, TARGET, CMD)

if CMD == "d":
    INPUT = readFile(TARGET, CMD)
    OUTPUT = decode(INPUT[0], INPUT[1])
    writeFile(OUTPUT, TARGET, CMD)
