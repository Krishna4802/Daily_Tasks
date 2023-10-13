# Program to print Hello World

print("Hello world !");


# Program to get number of words in 


# to install library
!pip install PyPDF2

#code to execute
from PyPDF2 import PdfReader
reader = PdfReader('/media/Krishna Prasath Resume (2).pdf')
page = reader.pages[0]
text = page.extract_text()
words = text.split()
print(len(words))
