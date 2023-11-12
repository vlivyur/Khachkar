import json
import os
import logging

class FileStorage:
    WorkingDir = "../Khachkar.Data/"

    def __init__(self) -> None:
        if not os.path.exists(self.WorkingDir):
            os.makedirs(self.WorkingDir)

    def FileNameGet(self, place):
        """ Generate file name

        Args:
            place (dict): description of the place

        Returns:
            str: file name: "Place.json" or "Place, Site.json"
        """
        filename = place["Place"]
        if (place["Site"] != ""):
            filename += ", " + place["Site"]
        filename += ".json"
        filename = os.path.join(self.WorkingDir, filename)
        return filename

    def ResultSave(self, place):
        """ Save to file

        Args:
            place (dict): what to save
        """
        s = json.dumps(place, indent = 4)
        filename = self.FileNameGet(place)
        try:
            with open(filename, 'w') as outxml:
                outxml.write(s)
            logging.info(f"Saved result to {filename}")
        except:
            logging.error(f"Can't save {filename}")
