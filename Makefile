
init: wine-reviews

wine-reviews.zip:
	kaggle datasets download -d zynicide/wine-reviews

wine-reviews: wine-reviews.zip
	mkdir wine-reviews
	unzip wine-reviews.zip -d wine-reviews

clean:
	rm -rf wine-reviews
	rm -rf wine-reviews.zip
