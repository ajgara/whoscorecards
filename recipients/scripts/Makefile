# Run make with a country code
# e.g. make COUNTRY=ALB

all: makepdf fixpdf

makepdf:
	phantomjs rasterize.js http://localhost:8000/oda/scorecard/front/$(COUNTRY)/ $(COUNTRY)_front.pdf 297mm*210mm
	phantomjs rasterize.js http://localhost:8000/oda/scorecard/back/$(COUNTRY)/ $(COUNTRY)_back.pdf 297mm*210mm

fixpdf:
	pdfjam $(COUNTRY)_front.pdf  --landscape --outfile $(COUNTRY)_front.pdf
	pdfjam $(COUNTRY)_back.pdf  --landscape --outfile $(COUNTRY)_back.pdf

