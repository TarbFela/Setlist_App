import os
import string
from difflib import SequenceMatcher


Genres = []
with open("genres_library.txt",'r') as f:
    Genres = [ line[:-1] for line in f]
print(Genres)

def get_file_paths(directory, ftype="pdf"):
    file_paths = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename[-3:] != ftype: continue
            file_paths.append(os.path.join(dirpath, filename))
    return file_paths

def name_cleanup(string):
    return string.lower().replace(
        "_", " "
    ).replace(
        "-", " "
    ).replace(
        "'", ""
    ).replace(
        "!", ""
    ).replace(
        "?", ""
    ).replace(
        ".", ""
    ).replace(
        "'",""
    ).replace(
        ",",""
    )
class Song:
    def __init__(self, name_string_input, get_pdfs = False):
        name = name_cleanup(name_string_input)
        #ADD ALTERNATE NAME SUPPORT (parenthitcals)

        self.name = name
        self.tags = {
            "isLearned": False,
            "genres": set(),
            "difficulty": None,
            "last_played": None,
        }
        if get_pdfs: self.find_pdfs()
        else: self.pdfs = []
        self.recording_links = []



    def find_pdfs(self, sim_thresh = 0.4, mode = "replace"):
        fps = get_file_paths("../")
        fps_weights = [
            SequenceMatcher(
                None, self.name, fp.split("/")[-1]
            ).ratio() for fp in fps
        ]
        match_fps = []
        for fp, sim in zip(fps, fps_weights):
            if sim > sim_thresh: match_fps.append(fp)
        if mode == "replace": self.pdfs = match_fps
        elif mode == "append": self.pdfs.append(match_fps)
        return match_fps


    def update_isLearned(self, learned : bool = True):
        self.tags["isLearned"] = learned

    def add_genres(self, genres):
        if type(genres) is str:
            genres = [genres]
        for genre in genres:
            if genre not in Genres: raise ValueError("provided genre was not in library")
            self.tags["genres"].add( genre )
    def remove_genres(self, genres):
        if type(genres) is str:
            genres = [genres]
        for genre in genres:
            if genre not in Genres: raise ValueError("provided genre was not in library")
            try:
                self.tags["genres"].remove( genre )
            except KeyError:
                print(f"{genre} was not found in song genres")
    @property
    def genres(self):
        return self.tags["genres"]

    def __str__(self):
        txt = ""
        #header
        header = "Song: " + self.name
        txt += header + "\n"
        #tags
        for key, value in zip(self.tags.keys(), self.tags.values()):
            if key == 'genres':
                txt += f'\t{key}: '
                for genre in value: txt += f'{genre}, '
                txt += "\n"
            else:
                txt += f'\t{key}: {value}\n'
        #pdfs
        txt += f'\tPDFs: '
        for pdf in self.pdfs:
            txt += f'{pdf}, '#f'{pdf.filepath}, '
        txt += "\n"
        #recording links
        txt += "\tRecordings: "
        for hyperlink in self.recording_links:
            txt += f'{hyperlink}, '
        txt += "\n"
        return txt
    def open_pdf(self, pdf_index = 0):
        os.system(f'open "{self.pdfs[pdf_index]}"')





class SongLibrary:
    def __init__(self, name = "SONG LIBRARY", songs = []):
        self.name = name
        self.songs = songs
    def save_to_file(self):
        with open(self.name + ".txt", 'w') as f:
            header = self.name
            f.write(header + "\n")
            for song in self.songs:
                f.write( str(song) )
    def __iter__(self, i):
        return self.songs[i]
    def __add__(self, other): #allows adding an arbitrary n of songs to lib w/ addition
        if type(other) != list:
           other = [other]
        for item in other:
            if type(item) != Song: raise TypeError ("could not add non-song to library")
            self.songs.append(item)
        return self
    def newsong(self, song_string):
        self += Song(
            song_string
        )

    def search_library(self, search_term):
        song_names = [song.name for song in self.songs]
        weights = [
            SequenceMatcher(
                None, name, search_term
            ).ratio() for name in song_names
        ]
        best_result_index = weights.index(max(weights))
        return self.songs[best_result_index]




song_library = SongLibrary()

def load_from_file(path = "SONG LIBRARY.txt"):
    SL = SongLibrary()
    newsong = None
    with (open(path, 'r') as f):
        lines = [line.replace("\n","") for line in f]
        for counter, line in enumerate(lines):
            #print(line)
            if counter == 0:
                SL.name = line
                continue
            if line[0:5] == "Song:":
                if newsong != None: SL.songs.append(newsong)
                newsong = Song(
                    name_string_input=line.replace(
                        "Song: ",""
                    ).replace(
                        "\n",""
                    )
                )
            if "PDFs:" in line:
                line_list = line.replace("\tPDFs: ","")
                line_list = line_list.split(", ")
                if line_list[-1] == '': del line_list[-1]
                #print(line_list)
                newsong.pdfs = line_list
                continue
            if "Recordings:" in line:
                line_list = line.replace("\tRecordings: ","")
                line_list = line_list.split(", ")
                if line_list[-1] == '': del line_list[-1]
                #print(line_list)
                newsong.recording_links = line_list
                continue
            if "genres:" in line:
                line_list = line.replace("\tgenres: ", "")
                line_list = line_list.split(", ")
                if line_list[-1] == '': del line_list[-1]
                line_set = set(line_list)
                #print(line_set)
                newsong.tags["genres"] = line_set
                continue
            if line[0] == "\t": #diff and islearned
                l_key, l_val = line.replace(
                    "\t",""
                ).replace(
                    " ",""
                ).split(":")
                #print(l_key)
                #print(l_val)
                newsong.tags[l_key] = l_val

        SL.songs.append(newsong)
        return SL



