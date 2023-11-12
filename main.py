from FileStorage import FileStorage
from ArmenicaParser import ArmenicaKhachkarParser
import logging

startURL = "https://www.armenica.org/cgi-bin/armenica.cgi?467864590376361=2=h"

logging.basicConfig(level = logging.INFO)
storedFiles = FileStorage()
# walk through the list of places
for place in ArmenicaKhachkarParser.PlacesGet(startURL):
    logging.info(f"Parsing location {place.Place}")
    # load first page of the place
    sp = ArmenicaKhachkarParser.UrlLoad(place.PlaceUrl)
    # get number of pages
    pagecount = ArmenicaKhachkarParser.PlacePageMaxCount(sp)
    # parse first page
    placeinfo = dict()
    placeinfo["Place"] = place.Place
    placeinfo["Site"] = place.Site
    placeinfo["Khachkars"] = ArmenicaKhachkarParser.PlacePageParse(sp)
    # load and parse other pages if any
    for pagenumber in range(2, pagecount):
        logging.info(f"Parsing location {place.Place} page {pagenumber}")
        sp = ArmenicaKhachkarParser.UrlLoad(ArmenicaKhachkarParser.PageNumberUrlGet(place.PlaceUrl, pagecount))
        placeinfo["Khachkars"] += ArmenicaKhachkarParser.PlacePageParse(sp)
    # store each place in separate file
    storedFiles.ResultSave(placeinfo)
