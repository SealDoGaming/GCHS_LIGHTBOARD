import os
import sys

from pydub import AudioSegment
from pydub.playback import play


#import pygame

on_pi = True
import RPi.GPIO as GPIO
from light import Light as Light
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import firebase_admin
from firebase_admin import credentials,firestore,storage
import pygame 
try:
    import cPickle as pickle
except:
    import pickle

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, r"Server Files")
service_dir = os.path.join(data_dir, r"ServiceFolder")
pattern_dir = os.path.join(data_dir, r"Patterns")
music_dir = os.path.join(data_dir, r"Music")
driver_dir = os.path.join(data_dir, r"WebDriverFiles")


sys.path.append(data_dir)
sys.path.append(service_dir)
sys.path.append(pattern_dir)
sys.path.append(music_dir)
sys.path.append(driver_dir)

#pinList = [11,12,13, 15, 16, 18, 22, 7]

pinList = [29,31,32,33,35,36,37,38]

pins = [29,31,32,33,35,36]

#file= open(os.path.join(data_dir,'SplashpageURL.txt'))
#file.close()

target_element_class='atn-button-text'
#'btn btn-default btn-lg atn-button atn-button-no-link atn-button-no-visible atn-plugin-clickthrough-button atn-plugin-movable-button'
#"atn-containing-form"
pygame.mixer.init()

class LightServer():
    def __init__(self,GPIO,lights):
        self.GPIO=GPIO
        self.lights = lights
        
        self.setup()
        #waits untill internet connection
        while not self.connected_to_internet():
            time.sleep(5)
            
        #self.bypass_splashpage()
        
        self.update()
        
        """ Work on making the part where it waits voting and plays the most voted thing"""
        #self.play_board("Blocks.ogg","speedyDash.pickle")
        #"Wilhelm Scream.wav"
        for i in range(5):
            self.play_board("Blocks.ogg","Speedy_Dash.pickle")
            time.sleep(1)
            print("and again")
            
        
        
        

    def setup(self):
        #pygame.mixer.init()
        cred = credentials.Certificate(os.path.join(service_dir,"gchs-lightboard-firebase-adminsdk-h2sjx-5d5a8f04aa.json"))
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.bucket_name = "gchs-lightboard.appspot.com"
        
        self.storage= storage.bucket(self.bucket_name)
        
        self.reader = PatternReader()
        
        #Ensures all the lights are off when starting up
        for i in range(len(self.lights)):
            self.lights[i].setState()
            #print(self.lights[i].state)
        
    def update(self):
        self.download_files(music_dir,u'music',"Music/")
        self.download_files(pattern_dir,u'light_patterns',"Patterns/")
        

    def connected_to_internet(self,url='http://www.example.com/', timeout=5):
        try:
            req= requests.head(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            print("No internet connection available.")
            //self.bypass_splashpage()
        return False
    
    def bypass_splashpage(self):
        driver = self.generate_webdriver()
        file = open(os.path.join(data_dir,"SplashpageURL.txt"))
        driver.get(file.read())
        file.close
        assert "Splash page" in driver.title
        elem = driver.find_element_by_class_name(target_element_class)
        print(elem)
        elem.click()
        time.sleep(5)
        driver.close()
        
    def generate_webdriver(self):
        driver=None
        if(sys.platform=='win32'):
            driver = webdriver.chrome.webdriver.WebDriver(executable_path=os.path.join(driver_dir,'chromedriver_windows'))
        elif(sys.platform=='darwin'):
            driver = webdriver.chrome.webdriver.WebDriver(executable_path=os.path.join(driver_dir,'chromedriver_mac'))
        else:
            driver = webdriver.chrome.webdriver.WebDriver(executable_path=os.path.join(driver_dir,'chromedriver_linux'))
        return driver
        
        
    def play_board(self,music_name,pattern_name):
        self.reader.load_pattern(os.path.join(pattern_dir,pattern_name))
        
        pygame.mixer.music.load(os.path.join(music_dir,music_name))
        pygame.mixer.music.play()
        
        #while pygame.mixer.music.get_busy():
        
        while pygame.mixer.music.get_busy():
            pin_value = self.reader.check_pattern()
            
            print(pin_value)
            
            for i in range(len(pin_value[1])):
                light_value = bool(pin_value[1][i])
                    
                print(i)
                self.lights[i].setState(light_value)
            light_string = ""
            gpio_string = ""
            for i in range(len(self.lights)):
                light_string = light_string + (" | "+str(self.lights[i].state))
                
            light_string += " | "
            print(light_string)
            #print(GPIO.logger)
            #print(self.GPIO.gpio_function(self.pins[0]))
            
    
    def download_files(self,location,collection,filepath):
        docs = self.db.collection(collection).stream()
        
        manifest= []
        
        for doc in docs:
            manifest.append(doc.get(u'id'))
        
        
        print("Loading: " +filepath.split("/")[0])
        for name in manifest:
            dest_location =os.path.join(location,name)
            if(not os.path.exists(dest_location)):
                try:
                    if(not os.path.exists(name)):
                        blob = self.storage.blob(filepath+name)
                        if(not name in os.scandir(location)):
                            blob.download_to_filename(dest_location)
                except:
                    print("Error Downloading: "+name)
            
            
        
        """
        blobs = self.storage.list_blobs( prefix=prefix, delimiter=delimiter)
        
        for blob in blobs:
            print(blob.name)

            if delimiter:
                print("Prefixes:")
                for prefix in blobs.prefixes:
                    print(prefix)
        
        for i in manifest:
            print(i)
        for blob in blobs:
            if delimiter:
                blob_location =os.path.join(location,blob.name)
                if(not blob.name in os.scandir(location)):
                    blob.download_to_filename(blob_location)
        """  
            
        
        
        
class PatternReader():
    
    def __init__(self,):
        self.pattern=None
        
    def load_pattern(self,pattern):
        try:
            
            file = open(os.path.join(pattern_dir,pattern),"rb")
            self.pattern =pickle.load(file)
            #print(self.pattern)
            file.close()
            #print(self.pattern)
        except:
            print(pickle.UnpicklingError)

    def valid_pattern(self):
        try:
            if(self.pattern==None):
                return False
                print("Invalid Pattern")
            elif(len(self.pattern[0]) != 2 and len(self.pattern[0][1])==5):
                return False
            else:
                return True
        except:
            print("Error")
        
    def check_pattern(self):
        if(self.valid_pattern()):
            #print(self.pattern)
            
            
            time.sleep(self.pattern[0][0])
            patternState = self.pattern.pop(0)
            self.pattern.append(patternState)
            return patternState

GPIO.setmode(GPIO.BOARD)
#print(GPIO.getmode())
pinList = [29,31,32,33,35,36,37,38]

for i in pinList:
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, True)

light1=Light(pinList[0],"1")
light2=Light(pinList[1],"2")
light3=Light(pinList[2],"3")
light4=Light(pinList[3],"4")
light5=Light(pinList[4],"5")
light6=Light(pinList[5],"6")
light7=Light(pinList[6],"7")
light8=Light(pinList[7],"8")
lights=[light4,light2,light7,light6,light5]

lights2 = [light1,light2,light3,light4,light5]



def main():
        
    #print("mouse")
    bill = LightServer(GPIO,lights2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()
