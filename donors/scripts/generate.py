#!/usr/bin/env python

import os, sys
from time import sleep
from pyPdf import PdfFileWriter, PdfFileReader

def donors(path='./data/'):
    donors = []
    for f in os.listdir(path):
        if f.endswith('.csv'):
            fd = open(path + f, 'r')
            _ = fd.readline()
            for line in fd.readlines():
                donor = line.split(',')[0]
                if donor not in donors and donor != 'totals':
                    donors.append(donor)
    return donors
    

def generate(donor):
    os.system('mkdir -p output')
    donor_url = donor.replace(' ','%20')
    page1 = 'output/%s1' % (donor.replace(' ','-').lower())
    page2 = 'output/%s2' % (donor.replace(' ','-').lower())
    combined = 'output/%s' % (donor.replace(' ','-').lower())
    os.system('cp svg/who_donor_page1.svg %s.svg' % (page1))
    os.system('sed "s|/France/|/%s/|" svg/who_donor_page1.svg > %s.svg' % (donor_url, page1))
    os.system('inkscape  --file=%s.svg --verb=za.co.widgetlabs.update --verb=FileSave --verb=FileQuit' % (page1))
    os.system('inkscape --file=%s.svg --export-pdf=%s.pdf' % (page1, page1))
    os.system('cp svg/who_donor_page2.svg %s.svg' % (page2))
    os.system('sed "s|/France/|/%s/|" svg/who_donor_page2.svg > %s.svg' % (donor_url, page2))
    os.system('inkscape --file=%s.svg --verb=za.co.widgetlabs.update --verb=FileSave --verb=FileQuit' % (page2))
    os.system('inkscape --file=%s.svg --export-pdf=%s.pdf' % (page2, page2))
    # Merge pages
    input1 = PdfFileReader(file('%s.pdf' % (page1), 'rb'))
    input2 = PdfFileReader(file('%s.pdf' % (page2), 'rb'))
    output = PdfFileWriter()
    output.addPage(input1.getPage(0))
    output.addPage(input2.getPage(0))
    outputStream = file('%s.pdf' % (combined), 'wb')
    output.write(outputStream)
    outputStream.close()
    sleep(2)

if __name__=="__main__":
    if len(sys.argv) == 1:
        for donor in donors():
            generate(donor)
    else:
        for donor in sys.argv[1:]:
            generate(donor)

