import PyPDF2 as pp
from PyPDF2 import PdfReader

def get_book_text(path):
    a=pp.PdfReader(path)
    # print(a.metadata) # Meta Data
    # print(len(a.pages)) # To get no of pages
    #print(a.pages[1]) # Return many objects
    #print(a.pages[i].extract_text) #1 is page number printed
    book_text=''
    for i in range(0,len(a.pages)):   
        book_text+=a.pages[i].extract_text()

    with open('book_text.txt','w',encoding='UTF-8') as f:
        f.write(book_text.lower())
    return book_text
