import argparse
import pandas as pd
import requests
import json
import traceback
import re

parser = argparse.ArgumentParser()
parser.add_argument("blanton_list")
parser.add_argument("output_list")
parser.add_argument("run_test")
args = parser.parse_args()



class ACC():
    def __init__(self, string):
        self.string = string

    def getYear(self):
        before_dot = self.string.split(".")[0]
        if(len(before_dot) > 4):
            return before_dot[1:]
        return before_dot 

    def getJPGLink(self):
        if ("/" not in self.string):
            return "https://collection.blantonmuseum.org/Media/images/ART%20New/{}/{}.jpg".format(self.getYear(), self.string) 
        
        return "https://collection.blantonmuseum.org/Media/images/ART%20New/{}/{}.jpg".format(self.getYear(), self.string.replace("/", "_"))
    
    def getPNGLink(self):
        if ("/" not in self.string):
            return "https://collection.blantonmuseum.org/Media/Previews/ART%20New/{}/{}.png".format(self.getYear(), self.string) 
        
        return "https://collection.blantonmuseum.org/Media/Previews/ART%20New/{}/{}.png".format(self.getYear(), self.string.replace("/", "_"))
        
    def getJSONLink(self):
        return "https://collection.blantonmuseum.org/results.html?&layout=objects&format=json&maximumrecords=-1&recordType=objects_1&query=mfs%20all%20%22{}%22".format(self.string)

input_file = None
try:
    input_file = pd.read_excel(args.blanton_list)
except:
    print("[!] Failed to open: " + args.blanton_list)
    exit(-1) 

print("[+] Opened file: " + args.blanton_list)

accessions = None
try:
    accessions = input_file['Accession #'].copy()
    if (accessions.size <= 1):
        raise Exception("[!] Accession # columns has less than or 1 member.")
except:
    print('[!] Failed to get column: Accession #')
    exit(-1)


if (str(args.run_test) == True):
    print("[+]: Running Tests!")
    known_results = [True, True, False, True, True]

    results = []
    try:
        images_found = 0
        hasimg_list = []
        for i, acc in accessions.iteritems(): 
            try:
                a = ACC(str(acc))


                j = requests.get(a.getJSONLink())
                j_clean = re.sub(",[ \t\r\n]+}", "}", j.text)
                j_clean = re.sub(",[ \t\r\n]+\]", "]", j_clean)
                j_json = json.loads(str(j_clean), strict=False)
                image_list = j_json['objects'][0]['Images']
                if (len(image_list) > 0):
                    images_found += 1
                    hasimg_list.append(True) 
                else:
                    hasimg_list.append(False)

                print("[+" + str(i) + "] " + a.string + " :: " + "IMAGE :: " + str(len(image_list)))
            except IndexError as e:
                print("[+" + str(i) + "] " + a.string + " :: " + "IMAGE :: " + "NO IMAGE, SKIPPING")
                hasimg_list.append(False)
             
        print("rows with images: " + str(images_found))

    except Exception as e:
        print("[!] Failed to loop over Accession #")
        print(traceback.format_exc())
   
    print("[!] Test Results: ", hasimg_list)
    print("[!] Known Results: ", known_results)
    print("We're done.")
    exit(0)

try:
    images_found = 0
    hasimg_list = []
    for i, acc in accessions.iteritems(): 
        try:
            a = ACC(str(acc))
            j = requests.get(a.getJSONLink())
            j_clean = re.sub(",[ \t\r\n]+}", "}", j.text)
            j_clean = re.sub(",[ \t\r\n]+\]", "]", j_clean)
            j_json = json.loads(str(j_clean), strict=False)
            image_list = j_json['objects'][0]['Images']
            if (len(image_list) > 0):
                images_found += 1
                hasimg_list.append(True) 
            else:
                hasimg_list.append(False)

            print("[+" + str(i) + "] " + a.string + " :: " + "IMAGE :: " + str(len(image_list)))
        except IndexError as e:
            print("[+" + str(i) + "] " + a.string + " :: " + "IMAGE :: " + "NO IMAGE, SKIPPING")
            hasimg_list.append(False)
             
    print("rows with images: " + str(images_found))

    input_file['image_found'] = hasimg_list
    input_file.to_excel(args.output_list)
    
    
except Exception as e:
    print("[!] Failed to loop over Accession #")
    print(traceback.format_exc())