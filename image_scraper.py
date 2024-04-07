from selenium import webdriver
import requests
from PIL import Image
import wget

import time
import io
import os
import sys
import zipfile
import stat


DRIVER_PATH = "./chromedriver"
DRIVER = "chromedriver"


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_time: float=1):
    """
    Selenium code to automate search and download
    """
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time)
        
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    
    # load the page
    wd.get(search_url.format(q=query))
    
    # set of image urls initialized to empty
    image_urls = set()
    image_count = 0
    results_start = 0
    
    while image_count < max_links_to_fetch:
        
        scroll_to_end(wd)
        
        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:
            # try clicking every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_time)
            except Exception as e:
                continue
                    
            # extract image urls
            actual_images = wd.find_elements_by_css_selector("img.n3VNCb")
            
            for actual_image in actual_images:
                if actual_image.get_attribute("src") and "http" in actual_image.get_attribute("src"):
                    image_urls.add(actual_image.get_attribute("src"))
                    
            image_count = len(image_urls)
            
            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        
            else:
                print(f"Found: {len(image_urls)} image links, looking for more ...")
                # time.sleep(30)
                
        load_more_button = wd.find_element_by_css_selector(".mye4qd")
        if load_more_button:
            wd.execute_script("document.querySelector('.mye4qd').click();")
      
        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path:str, url:str, label:int):
    """ Download and save images """
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
    
    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
        file_path = os.path.join(folder_path, str(label) + ".jpg")
        
        with open(file_path, "w") as f:
            image.save(f, "JPEG", quality=85)
            
        print(f"Success - saved {url} as {file_path}")
        
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")
        

def search_and_download(search_term:str, driver_path:str, number_images=5):
    target_folder = '_'.join(search_term.lower().split(' '))

    # create download folder if it does not already exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # download chrome driver if it's not already in place
    if not os.path.exists(driver_path):
        if sys.platform.startswith("linux"):
            wget.download("https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip",
                          out="driver.zip")
        elif sys.platform.startswith("win32"):
            wget.download("https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_win32.zip",
                          out="driver.zip")
        elif sys.platform.startswith("darwin"):
            wget.download("https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_mac64.zip",
                          out="driver.zip")
        else:
            sys.exit("No supported chrome driver version for current OS!")

        # unzip downloaded zip file
        with zipfile.ZipFile("driver.zip") as zip_fptr:
            zip_fptr.extract(DRIVER)
            # give execute permission
            st = os.stat(DRIVER)
            os.chmod(DRIVER, st.st_mode | stat.S_IEXEC)

        # remove the zip file
        os.remove("driver.zip")

    # Automate search with Chrome driver and Selenium
    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_time=0.5)

    # Download and save selected images
    for label, elem in enumerate(res):
        persist_image(target_folder, elem, label+1)
        

if __name__ == "__main__":
    search_term = sys.argv[1]
    number_of_images = int(sys.argv[2])
    
    search_and_download(search_term=search_term,
                        driver_path=DRIVER_PATH,
                        number_images=number_of_images)