# Run make with a country code
# e.g. make COUNTRY=ALB

# or for all countries
# for iso in `cut -f1 -d, ../data/countries.csv`
# do               
# make COUNTRY=$iso
# done

all: makepdf fixpdf

makepdf:
	phantomjs rasterize.js http://localhost:8000/oda/scorecard/front/$(COUNTRY)/ $(COUNTRY)_front.pdf 380mm*270mm
	phantomjs rasterize.js http://localhost:8000/oda/scorecard/back/$(COUNTRY)/ $(COUNTRY)_back.pdf 380mm*270mm

fixpdf:
	pdfjam $(COUNTRY)_front.pdf  --landscape --outfile $(COUNTRY)_front.pdf
	pdfjam $(COUNTRY)_back.pdf  --landscape --outfile $(COUNTRY)_back.pdf

