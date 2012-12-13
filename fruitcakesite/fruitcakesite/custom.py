# Custom FileStorage class to turn off automatic creation of duplicate files with "_x" appended;
# See Burhan Khailid answer in 
# http://stackoverflow.com/questions/8332443/set-djangos-filefield-to-an-existing-file

from django.core.files.storage import FileSystemStorage

class MyFileStorage(FileSystemStorage):
    # this method is actually defined in Storage
    def get_available_name(self, name):
        return name #simply returns the name passed

