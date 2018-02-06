from constants import *


class Sheet(list):
    """ should be a 'time sequence' of an ordered set of notes """
    def __init__(self, tempo=2):
        self.tempo = tempo
        self.time = 0
        self.note_times = []
        
    def begin(self):
        self.time = SHEET_MARGIN * 1000
        
    def append(self, note):
        start, end = self.time, self.time + note.duration * 1000 * self.tempo
        self.note_times.append((start, end))
        self.time += end - start
        super(Sheet, self).append(note)
        
    def end(self):
        self.time += (SHEET_MARGIN * 1000)

    """the length of piece of music in millisec."""
    def __len__(self):
        return int(self.time)
    
    def  __str__(self):
        #return list.__str__(self)
        return str([(self[i], self.note_times[i]) for i in range(len(self.note_times))])
    

class Note():    
    def __init__(self, pitch, duration):
        self.pitch = pitch 
        self.duration = duration
        
    def __str__(self):
        return 'Note {} {}s'.format(self.pitch, self.duration)
    
    __repr__ = __str__
    


def frere_jacques():
    sheet = Sheet()
    sheet.begin()
    sheet.append(Note(55, QUARTER))
    sheet.append(Note(57, QUARTER))
    sheet.append(Note(59, QUARTER))
    sheet.append(Note(55, QUARTER))
    
    """sheet.append(Note(55, QUARTER))
    sheet.append(Note(57, QUARTER))
    sheet.append(Note(59, QUARTER))
    sheet.append(Note(55, QUARTER))
    
    sheet.append(Note(59, QUARTER))
    sheet.append(Note(60, QUARTER))
    sheet.append(Note(62, HALF))
    
    sheet.append(Note(59, QUARTER))
    sheet.append(Note(60, QUARTER))
    sheet.append(Note(62, HALF))
    
    sheet.append(Note(62, EIGHT))
    sheet.append(Note(64, EIGHT))
    sheet.append(Note(62, EIGHT))
    sheet.append(Note(60, EIGHT))
    sheet.append(Note(59, QUARTER))
    sheet.append(Note(55, QUARTER))
    
    sheet.append(Note(62, EIGHT))
    sheet.append(Note(64, EIGHT))
    sheet.append(Note(62, EIGHT))
    sheet.append(Note(60, EIGHT))
    sheet.append(Note(59, QUARTER))
    sheet.append(Note(55, QUARTER))
    
    sheet.append(Note(55, QUARTER))
    sheet.append(Note(50, QUARTER))
    sheet.append(Note(55, HALF))
    
    sheet.append(Note(55, QUARTER))
    sheet.append(Note(50, QUARTER))
    sheet.append(Note(55, HALF))"""
    sheet.end()
   
    return sheet
    
    
if __name__ == '__main__':
    sheet = frere_jacques()
    print(len(sheet))
    print(sheet)
    