import urllib
import requests

def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    return bookascii.split()

def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):

    words = book_to_words(book_url)
    buckets = []
    for _ in range(257):
        buckets.append([])

    for word in words:
        byte = 0
        if len(word) > 0:
            byte = word[0] + 1
        buckets[byte].append(word)
    
    final_arr = []
    for bucket in buckets:
        ancestors = [[bucket, 1]]
        while len(ancestors) > 0:
            x = ancestors.pop()
            arr = sortAt(x[1], x[0])
            final_arr += arr[0]
            for i in range(len(arr) - 1, 0, -1):
                y = [arr[i], x[1] + 1]
                if arr[i]:
                    ancestors.append(y)
    
    for i in range(len(final_arr)):
        final_arr[i] = final_arr[i].decode()

    return final_arr

def sortAt(index=0, bucket=[]):

    buckets = []
    for _ in range(257):
        buckets.append([])

    for el in bucket:
        byte = 0
        if len(el) > index:
            byte = el[index] + 1
        buckets[byte].append(el)

    return buckets

def main():
    print(radix_a_book())

main()