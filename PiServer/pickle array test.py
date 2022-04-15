import os
import sys
try:
    import cPickle as pickle
except:
    import pickle

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, r"Server Files")
service_dir = os.path.join(data_dir, r"ServiceFolder")
pattern_dir = os.path.join(data_dir, r"Patterns")
music_dir = os.path.join(data_dir, r"Music")

sys.path.append(data_dir)
sys.path.append(service_dir)
sys.path.append(pattern_dir)
sys.path.append(music_dir)



blink_list =[
        [0.125,[1,0,0,0,0]],
        [0.125,[0,1,0,0,0]],
        [0.125,[0,0,1,0,0]],
        [0.125,[0,0,0,1,0]],
        [0.125,[0,0,0,0,1]],]
file = open(os.path.join(pattern_dir,"speedyDash.pickle"),"wb")
pickle.dump(blink_list,file)
file.close()