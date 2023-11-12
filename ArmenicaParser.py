from pathlib import Path
from bs4 import BeautifulSoup, Tag #pip install beautifulsoup4
import requests #pip install requests
from enum import Enum
from os import path
from urllib import parse

class PartOfDescription(Enum):
    """ Indicates which part is parsing now
    """
    StartingPoint = 0
    KhachkarName = 1
    Attribute = 2
    AttributeValue = 3

class PlacePage:
    """ Description of location and URL of its first page
    """
    def __init__(self) -> None:
        self.Place = ""
        self.Site = ""
        self.PlaceUrl = ""
    
class ArmenicaKhachkarParser:
    """ Parser of armenica's pages
    """
    def PlacesGet(mainpageurl):
        """ Parsing navigation tree for locations and their URLs

        Args:
            mainpageurl (str): starting page of "Kchatchkars"

        Returns:
            PlacePage[]: list of all places
        """
        sp = ArmenicaKhachkarParser.UrlLoad(mainpageurl)
        locations = []
        for locationUrl in sp.find_all(name = "a", class_ = 'm'):
            place = PlacePage()
            place.Place = locationUrl.contents[0].split('(')[0].strip()
            if "," in place.Place:
                place.Site, place.Place = [s.strip() for s in place.Place.split(',')]
            place.PlaceUrl = locationUrl.attrs["href"]
            locations.append(place)
        return locations
    
    def PageNumberUrlGet(firstpage, pagenumber):
        """ Gets URL for pages number >= 2

        Args:
            firstpage (str): URL of the first page of the place
            pagenumber (int): number of the page

        Returns:
            str: URL with included page number
        """
        return firstpage + "====0=" + str(pagenumber)
    
    def UrlLoad(url):
        """ Gets BeautifulSoup object for given URL

        Args:
            url (str): URL of the page

        Returns:
            BeautifulSoup: object for given URL
        """
        page = requests.get(url)
        sp = BeautifulSoup(page.text, "html.parser")
        return sp
    
    def PlacePageMaxCount(bsFirstPage):
        """ Find number of last page for this place

        Args:
            bsFirstPage (BeautifulSoup): first page of the place

        Returns:
            int: last page number
        """
        pages = bsFirstPage.find(name = "td", class_ = "contentnormal5").contents
        lastpage = 1
        for s in reversed(pages):
            if isinstance(s, Tag):
                lastpage = int(s.contents[0])
                break
        return lastpage

    def PlacePageParse(bsPage):
        """ Parsing of any page of the place

        Args:
            firstpageurl (str): URL of first page of the place (without page number)
            pagenumber (int): number of the page

        Returns:
            Khachkar[]: list of found on the page khachkars
        """
        kl = list()
        # parse the first page of the place
        for k in bsPage.find_all(name = "td", class_ = "contentnormal3"):
            # description of each khachkar is divided onto two parts: picture and description
            if "width" in k.attrs: # right (and last) part with description
                whichPart = PartOfDescription.StartingPoint
                numberOfAttribute = 0
                key = ""
                value = ""
                for d in k.contents:
                    if d in ("\n", " Click on image to enlarge\n") or isinstance(d, Tag) and d.name == "br":
                        continue
                    if isinstance(d, Tag) and d.name == "b":
                        if whichPart == PartOfDescription.StartingPoint:
                            whichPart = PartOfDescription.KhachkarName
                        elif whichPart == PartOfDescription.KhachkarName:
                            desc["Name"] = key.strip()
                            whichPart = PartOfDescription.Attribute
                        elif whichPart == PartOfDescription.Attribute:
                            numberOfAttribute += 1
                            desc["UnknownAttribute" + str(numberOfAttribute)] = key.strip()
                            whichPart = PartOfDescription.Attribute
                        else:
                            whichPart = PartOfDescription.Attribute
                        key = d.text
                        continue
                    elif isinstance(d, str):
                        numberOfAttribute += 1
                        if whichPart == PartOfDescription.StartingPoint:
                            key = "Name"
                        elif whichPart == PartOfDescription.KhachkarName:
                            value = key
                            key = "Name"
                        elif whichPart == PartOfDescription.AttributeValue:
                            key = "UnknownAttribute" + str(numberOfAttribute)
                        #if whichPart != PartOfDescription.StartingPoint:
                        value = d.strip(": ")
                        if value == "N/A":
                            value = ""
                        desc[key] = value.strip()
                        whichPart = PartOfDescription.AttributeValue
                # parse khachkarText
                for description in khachkarText:
                    numberOfAttribute += 1
                    if ":" not in description:
                        if "Description" in desc:
                            key = "UnknownAttribute" + str(numberOfAttribute)
                        else:
                            key = "Description"
                        value = description
                    else:
                        key, value = description.split(":")
                    value = value.strip()
                    if value == "N/A":
                        value = ""
                    if key in desc and desc[key] == "" and value != "" or key not in desc:
                        desc[key] = value
                # everything of this khachkar is collected
                kl.append(desc)
            else: # left part with image
                desc = dict()
                imgurl = k.find(name = "a", class_ = "highslide")
                if imgurl != None:
                    pictureUrl = imgurl.attrs["href"]
                    desc["ImageUrl"] = pictureUrl
                    khachkarText = k.text.strip().split("\n")
            
        return kl