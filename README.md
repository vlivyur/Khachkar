# What is it for?
It's a parser of khachkars from https://www.armenica.org/. Made for [The Open Data Armenia team](https://github.com/opendataam/opendatam-tasks/issues/28).

# Installation
It requires requests and BeautifulSoup:
```bash
pip install requests beautifulsoup4
```

# Description of output format
```json
{
    "Place": "Bjni",
    "Site": "Holy Virgin",
    "Khachkars": [
        {
            "ImageUrl": "https://www.armenica.org/collection/khatchkar/Akhtamar-Van/aghtamar-kk07a-kkb.jpg",
            "Name": "Khatchkar",
            "Location": "Akhtamar (Van)",
            "Origin": "Ambert",
            "Sculptor": "Vahram",
            "Date": "14-C",
            "Description": "The khatchkar on the side of western entrance of the church St Grigor Lousavorictch",
            "Source": "Suren Manvelyan"
        }
    ]
}
```
Output directory for files is Khachkar.Data
- Place - menu item from the navigation menu
- Site - first part of menu item if Place contains ",", and empty if not. For "Holy Virgin, Bjni" here will be Holy Virgin and Place will be Bjni
- Khachkars - list of all khachkars from all pages of the place
    - ImageUrl - URL of full image
    - Name - first line from description on the right. It could be written in regular font or just bold "Khatchkar" without name
    - Location - line Location: from description on the right. Slightly differs from Place
    - Origin - line Origin: from description on the right. Probably, a place where it was before, but it repeats Place (Ambert and Ambert)
    - Sculptor - line Sculptor: from description on the right or from popup with enlarged image. As for now there is just Vahram in Haghpat
    - Date - line Date: from description on the right or from popup with enlarged image. Year (100) or century (13-C) of the khachkar
    - Description - first line from popup with enlarged image
    - Source - from popup with enlarged image. Probably, author of the picture
N/A in values replaced with empty line