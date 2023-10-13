# Pdf-word-count


1. Download docker desktop 


# Commands

2. In terminal

* To install ubuntu       : docker pull ubuntu:latest
* To run docker container : docker run -it -p 8888:8888 --name sample ubuntu


3. In Docker terminal

* To get updates           : apt-update
* To install python latest : apt install python3
* To install pip3          : apt install pip3
* To install Notebook      : pip3 install Jupyter
* To install nano          : apt install nano
* To run notebook in browser : jupyter-notebook --allow-root --ip=0.0.0.0
* Then open the link display in therminal in chrome (http://127.0.0.1:8888/notebooks/Untitled.ipynb?kernel_name=python3) it will open Jupyter notebook in that code.


4. Place the pdf file in Media folder in Ubuntu Container
    Location of file : /media/Krishna Prasath Resume (2).pdf

5. In chrome - Jupyter Notebook

 # Python code to print Hello world

    print("Hello World !")

* To install the library for processing pdf : !pip install PyPDF2

# Python code for fetching no.of words from PDF

    from PyPDF2 import PdfReader
    reader = PdfReader('/media/Krishna Prasath Resume (2).pdf')
    page = reader.pages[0]
    text = page.extract_text()
    words = text.split()
    print(len(words))
