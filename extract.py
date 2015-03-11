#!/usr/bin/env python

import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage

def extract_pdf(in_file_name, out_file_name):

  # File definitions, openings
  ##
  in_file = open(in_file_name, "rb")
  out_file = open(out_file_name, "wb")

  # Declaration of the relevant PDF classes
  ##
  resource = PDFResourceManager()
  device = TextConverter(resource, out_file, codec="utf-8", laparams=LAParams())
  ## device = XMLConverter(resource, out_file, codec="utf-8", laparams=LAParams())
  ## device = HTMLConverter(resource, out_file, codec="utf-8", laparams=LAParams())
  parser = PDFParser(in_file)
  document = PDFDocument(parser)
  ## Associates the PDF parser with a PDF document
  parser.set_document(document)
  interpreter = PDFPageInterpreter(resource, device)

  # The extraction
  ##
  for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
  in_file.close()
  out_file.close()

def main(in_path, out_path):

  import glob
  import os
  import time
  print "Checking input path for files: {0}".format(in_path)
  list_of_files = glob.glob("{0}*.pdf".format(in_path))
  print "Total number of PDFs: {0}".format(len(list_of_files))

  times = []
  with open('extract.log', 'w') as log:

    for in_file in list_of_files:

      in_file_raw = os.path.basename(in_file)
      TXT = in_file_raw.replace('.pdf', '.txt')
      out_file = os.path.join(out_path, TXT)
      print "Extracting the following PDF: {0}".format(in_file)
      print "Writing to TXT file: {0}".format(out_file)
      time_start = time.time()
      extract_pdf(in_file, out_file)
      time_stop = time.time()
      time_taken = time_stop - time_start
      times.append(time_taken)
      print "Time taken: {0} sec".format(time_taken)
      print ""
      log.write("{0} {1}\n".format(in_file_raw, time_taken))

    log.write("# Average time taken: {0} sec".format(sum(times)/(1.0*len(times))))

if __name__ == "__main__":

  import argparse
  parser = argparse.ArgumentParser(description='Run PDFMiner on some PDFs.')
  parser.add_argument('-i', '--in_path', dest='in_path', help='path to the list of PDFs', required=True)
  parser.add_argument('-o', '--out_path', dest='out_path', help='path to the output', required=True)

  args = parser.parse_args()

  main(args.in_path, args.out_path)
