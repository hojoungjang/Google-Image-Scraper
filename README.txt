Google Image Web Scraper!

What is it?
I was inspired to automate the tedious job of collecting images of plastic bottles for my machine learning project.
This Python script will let you download multiple images of Google Image search result.
But this does not verify the content of images!
It focuses on quickly gathering relevant and multiple images of your target search!

Requirements:
1. Highly recommend using Python 3.6 or higher (I tested on Python 3.8)
2. Make sure Chrome browser is up-to-date (to update, open Chrome browser -> go to 'settings' -> click 'About Chrome')
3. Run 'pip install -r requirements.txt' or 'pip3 install -r requirements.txt'

How to run:
1. use either python or python3 depending on python installed on your system
2. run the image_scraper.py script
3. the first argument is the search string (this is what you would type on Google search bar)
4. the second argument is the number of images you want to download

    example:
        python image_scraper.py <search string> <number of images>
        python3 image_scraper.py <search string> <number of images>

What happens?
1. It will create a folder named after your search string. (Images will be downloaded here)
2. It will download Chrome driver (if you do not have one) necessary for running Selenium.
3. It will open up Chrome browser, search and save URLs to images.
4. It will download images and save them inside the folder created at step 1.