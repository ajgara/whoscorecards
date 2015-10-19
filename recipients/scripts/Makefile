# Run make with a COUNTRY_ISO code
# e.g. make COUNTRY_ISO=ALB

all: makepdf fixpdf

makepdf:
	phantomjs rasterize.js http://localhost:8000/oda/scorecard/front/$(COUNTRY_ISO)/ ./output/$(COUNTRY_ISO)_front.pdf 376mm*267mm
	phantomjs rasterize.js http://localhost:8000/oda/scorecard/back/$(COUNTRY_ISO)/ ./output/$(COUNTRY_ISO)_back.pdf 376mm*267mm

fixpdf:
	# Following 2 lines commented by BSG
	# Glue front+back as: ISO_CountryName.pdf
	# pdfjam ./output/$(COUNTRY_ISO)_front.pdf ./output/$(COUNTRY_ISO)_back.pdf --landscape --outfile "./output/$(COUNTRY_ISO)_$(COUNTRY_NAME).pdf"
	# Glue front+back as: CountryName.pdf
	pdfjam ./output/$(COUNTRY_ISO)_front.pdf ./output/$(COUNTRY_ISO)_back.pdf --landscape --outfile "./output/$(COUNTRY_NAME).pdf"
	rm ./output/$(COUNTRY_ISO)_front.pdf ./output/$(COUNTRY_ISO)_back.pdf

#376mm*267mm LAST
#380mm*270mm
