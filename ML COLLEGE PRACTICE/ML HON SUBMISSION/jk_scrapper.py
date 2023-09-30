from bs4 import BeautifulSoup
import os
import requests
from fpdf import FPDF
from PIL import Image
import shutil



def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')
   # print out some text


response = requests.get("https://jujustukaisen.com/")
htmlContent = response.text
parsed_html = BeautifulSoup(htmlContent,"html.parser")
links = parsed_html.body.find(id="ceo_latest_comics_widget-3")
links = list(links.findAll("a"))
links.reverse()
incomplete = open("inc.txt","w")
epi_num=1
current_directory = os.getcwd()
for link in links:
    fileName = "episode_"+str(epi_num)+".pdf"
    if(not os.path.exists(os.path.join(current_directory, fileName))):
        epi = requests.get(link['href'])
        epi_html = epi.text
        epi_parsed = BeautifulSoup(epi_html,"html.parser")
        pages = epi_parsed.body.select('img[alt*="Jujutsu Kaisen, Chapter"]')
        #pages = pages.findAll("p")
        temp_dir_path = os.path.join(current_directory, r'.temp')
        if os.path.exists(temp_dir_path):
            shutil.rmtree(temp_dir_path)
        temp_dir = os.makedirs(temp_dir_path)
        pdf = FPDF(unit='mm')
        pdf.add_page()
        l = len(pages)
        i = 1
        print("Downloading episode - "+str(epi_num)+" number of pages: "+str(l))
        for page in pages:
            print(page['alt'])
            src = page['src']
            if src.endswith(".jpg") or src.endswith(".jpeg"):
                filePath = os.path.join(temp_dir_path,"page-"+str(i)+".jpg")
            else:
                filePath = os.path.join(temp_dir_path,"page-"+str(i)+".png")
            file = open(filePath,'wb')
            file.write(requests.get(src).content)
            img = Image.open(filePath)
            w,h = img.size
            w,h = float(w * 0.264583), float(h * 0.264583)
            pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
            orientation = 'P' if w < h else 'L'
            w = w if w < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
            h = h if h < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
            pdf.add_page(orientation=orientation)
            pdf.image(filePath, 0, 0, w, h)
        #             print(src+" "+str(i)+" ")
            i+=1
            img.close()
            file.close()
        if l==(i-1):
            screen_clear()
        else:
            incomplete.write("episode_"+str(epi_num)+"\n")
            screen_clear()
            print(str(l)+" "+str(i))
        pdf.output(fileName,"F")
        print("\n")
    else:
        print(fileName+" already exists moving to next")
    epi_num+=1

