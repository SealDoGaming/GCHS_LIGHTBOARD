import os
import io
try:
    import cPickle as pickle
except:
    import pickle

from google.cloud import storage

def add_music(db,main_storage,filename,title,song_id,artist,minutes,seconds):
    if(song_id!="" and title!="" and (minutes*60+seconds)>0):
        song = db.collection(u'music').document(song_id)
        song.set({
            u'Name':title,
            u'id':song_id,
            u'Artist':artist,
            u'length':minutes*60+seconds,
            
        })
        music_votes= db.collection(u'music_votes').document(song_id)
        music_votes.set({
            u'votes':0,
            
        })
        #storage_client = storage.Client(credentials=cred)
        blob = main_storage.blob('Music/'+song_id)
        #with open(filename, "rb") as file_obj:
        #    print(os.fstat(file_obj.fileno()).st_size)
        blob.upload_from_filename(filename,)

        print(
            "File {} uploaded to {}.".format(
                filename, 'Music/'+song_id
            )
        )
#def add_pattern_file(db,main_storage,filename,title):
def add_pattern(db,main_storage,pattern,title):
    
    pickled_pattern = io.BytesIO(pickle.dumps(pattern))
    #print(pattern)
    
    #print(pickle.load(pickled_pattern))
    
    pattern_id=title.replace(" ","_")+".pickle"
    if(pattern_id!="" and title!=""):
        pattern = db.collection(u'light_patterns').document(pattern_id)
        pattern.set({
            u'Name':title,
            u'id':pattern_id,
            
        })
        pattern_votes= db.collection(u'light_patterns_votes').document(pattern_id)
        pattern_votes.set({
            u'votes':0,
            
        })
        #storage_client = storage.Client(credentials=cred)
        blob = main_storage.blob('Patterns/'+pattern_id)
        #with open(filename, "rb") as file_obj:
        #    print(os.fstat(file_obj.fileno()).st_size)
        blob.upload_from_file(pickled_pattern)

        print(
            "File {} uploaded to {}.".format(
                pickled_pattern, 'Patterns/'+pattern_id
            )
        )
    