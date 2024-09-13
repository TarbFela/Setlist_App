from SetlistModule import *
i = 0
mysong = Song("Dolphin song")
mysong.add_genres(["hard_bop","jazz"])
mysong.pdfs = ["somefilepath.pdf", "anotherpath.pdf"]
mylib = SongLibrary(songs = [mysong])
mylib.save_to_file()

mylib = None
mylib = load_from_file()

print("THE LIBARAY IS")
for song in mylib.songs:
    print(song)
