#!/usr/bin/python
import os

file_names = sorted(os.listdir("./output/"))
# pdf_file_names_arg = " ".join(map(lambda x: "./output/" + x, file_names))
pdf_file_names_arg = " ".join(map(lambda x: "./output/" + "\"" + x + "\"", file_names))
# pdf_file_names_arg = " ".join(map(lambda x: "./output/" + str.replace(str.replace(str.replace(x,"(","\("),")","\)"),"'","\'"), file_names))

print("Joining %s " % pdf_file_names_arg)
os.system("pdfjoin %s --outfile all_countries.pdf" % pdf_file_names_arg)
os.system("pdf90 all_countries.pdf")