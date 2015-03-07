#!/usr/bin/env python

import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage

def main():

  resource = PDFResourceManager()

  out_file = StringIO.StringIO()
  out_file = open("alessia.html", "wb") 

  in_file = open("alessia.pdf", "rb")

  #device = TextConverter(resource, out_file, codec="utf-8", laparams=LAParams())
  #device = XMLConverter(resource, out_file, codec="utf-8", laparams=LAParams())
  device = HTMLConverter(resource, out_file, codec="utf-8", laparams=LAParams())


  parser = PDFParser(in_file)

  document = PDFDocument(parser)

  # Associates the PDF parser with a PDF document
  parser.set_document(document)

  interpreter = PDFPageInterpreter(resource, device)

  for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
  in_file.close()
  out_file.close()
 # print out_file.getvalue()

if __name__ == "__main__":
  main()
