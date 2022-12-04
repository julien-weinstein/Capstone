working_dir = 'C:/Users/JWeinstein/Capstone-main/src'

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import time
import os
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

# keyword_matches returns True if one of the following is True:
# - Anchor text starts with the keyword
# - Anchor text contains a space followed by the keyword followed by a space
# - Anchor text contains a space followed by the keyword
# - Anchor text ends with a space followed by the keyword
# - Text within the URL starts with the keyword
# - Text within the URL contains an underscore followed by the keyword followed by an underscore
# - Text within the URL contains an underscore followed by the keyword
# - Text within the URL ends with an underscore followed by the keyword

def keyword_matches(keyword, url_text, href_url):
    return url_text.startswith(keyword) or url_text.endswith(' '+keyword) or ' '+keyword+' ' in url_text or ' '+keyword in url_text or href_url.startswith(keyword) or href_url.endswith('_'+keyword) or '_'+keyword+'_' in href_url or '_'+keyword in href_url


def spider(seed_url, keyword, crawl_depth):

    # Wiki Main Page, which needs to be excluded while crawling
    main_page = 'https://en.wikipedia.org/wiki/Main_Page'
    # Count of number of URLs crawled
    crawled_count = 0
    # Maximum depth of crawling reached
    max_depth = 1

    # Frontier - A list of URLS depicting a queue containing next URLs to be crawled
    #          - will contain the seed URL initially
    frontier_urls = [seed_url]
    # Seen - A list of URLs containing URLs crawled, empty initially
    seen_urls = []

    # creation of Logs directory, if not present
    newpath = working_dir + r'Logs' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # creation of Raw_TXT_Downloads directory, if not present (commented below)

    newpath = working_dir + r'Raw_TXT_Downloads'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Mentioning the seed URL and keyword in focused_crawler_log.txt
    focused_crawler_log = open(working_dir + "Logs/focused_crawler_log.txt","w")
    focused_crawler_log.write("Seed : "+seed_url+"\n")
    focused_crawler_log.write("Keyword : "+keyword+"\n\n")

    # Writing into log file starting with Depth 1
    focused_crawler_log.write("Depth 1 :\n\n")
    crawled_count+=1
    focused_crawler_log.write(str(crawled_count)+") "+seed_url+"\n\n")

    # flag is True iff the limit of 1000 URLS has not been reached
    flag = True
    print("\n----------------------------------------- At depth 1--------------------------------------------------------")
    print(str(crawled_count)+") "+seed_url)

    # download web page into a txt file
    name = seed_url[seed_url.rfind('/')+1:]
    # Specify url of the web page, here: seed_url 
    source = urlopen(seed_url).read()
    # Make a soup 
    soup = BeautifulSoup(source,'lxml')
    # Extract the plain text content from paragraphs
    text = ''
    for paragraph in soup.find_all('p'):
        text += paragraph.text
    # Clean text
    text = re.sub(r'\[.*?\]+', '', text)
    text = text.replace('\n', '')
    # get title of the wikipedia article
    page_title = soup.find_all('title')[0].text[:-12]
    file = open(working_dir + "Raw_TXT_Downloads/"+(str(crawled_count))+") "+name+".txt","w", encoding='utf-8')
    file.write(seed_url + '\n' + page_title + '\n' + text)
    file.close()

    # assuming maximum depth to crawl as Depth 3
    for depth in range (2, crawl_depth+1):
        if flag:
            print("\n----------------------------------------- At depth "+str(depth)+"--------------------------------------------------------")
            focused_crawler_log.write("Depth "+str(depth)+" :\n\n")
            extracted_urls = []

            # Traversing through all the URLs to be crawled as pointed by the Frontier
            for frontier_url in frontier_urls:

                # Enter only if limit of 1000 URLs not reached
                if flag:

                    # get the soup
                    disable_warnings(InsecureRequestWarning)
                    source_code = requests.get(frontier_url, verify = False)
                    plain_text = source_code.text
                    soup = BeautifulSoup(plain_text,"html.parser")

                    # Filter URLs, choose only the ones starting with '/wiki/'
                    for link in soup.find_all('a', href=re.compile('^/wiki/')):

                        # check if limit reached or not
                        if crawled_count < 1000 and flag:

                            # retrieve the Anchor text and Text of the URL
                            url_text = link.text
                            href_url = link.get('href')
                            truncated_href_url = href_url[6:]

                            # Call helper function to check if keyword matches or not
                            if keyword_matches(keyword, url_text, truncated_href_url):

                                # Ignore all the Administrative URLs
                                if ':' not in href_url:

                                    # Handle URLs with '#' seperately
                                    if '#' not in href_url:
                                        url = 'https://en.wikipedia.org'+href_url

                                        # URL should not be in either of Frontier, Extracted or Seen lists and should not be Wiki Main Page too
                                        if url not in frontier_urls and url not in extracted_urls and url not in seen_urls and url != main_page:
                                            
                                            # Respecting the Politeness Policy
                                            time.sleep(0.2)

                                            # download web page into a txt file
                                            name = url[url.rfind('/')+1:]                                            
                                            # Specify url of the web page, here: url 
                                            source = urlopen(url).read()
                                            # Make a soup 
                                            soup = BeautifulSoup(source,'lxml')
                                            # Extract the plain text content from paragraphs
                                            text = ''
                                            for paragraph in soup.find_all('p'):
                                                text += paragraph.text
                                            # Clean text
                                            text = re.sub(r'\[.*?\]+', '', text)
                                            text = text.replace('\n', '')
                                            # get title of the wikipedia article
                                            page_title = soup.find_all('title')[0].text[:-12]
                                            file = open(working_dir + "Raw_TXT_Downloads/"+(str(crawled_count+1))+") "+name+".txt","w", encoding='utf-8')
                                            file.write(url + '\n' + page_title + '\n' + text)
                                            file.close()
                                            
                                            extracted_urls.append(url)
                                            crawled_count+=1
                                            focused_crawler_log.write(str(crawled_count)+") "+url+"\n")
                                            print(str(crawled_count)+") "+url)

                                    else:
                                        # Handle URLs with '#'
                                        hash_pos = href_url.index('#')

                                        # Trim the URL from the start till index before '#'
                                        url = 'https://en.wikipedia.org'+href_url[:hash_pos]

                                        # URL should not be in either of Frontier, Extracted or Seen lists and should not be Wiki Main Page too
                                        if url not in frontier_urls and url not in extracted_urls and url not in seen_urls and url != main_page:
                                            
                                            # Respecting the Politeness Policy
                                            time.sleep(0.2)

                                            # download web page into a txt file
                                            name = url[url.rfind('/')+1:]                                            
                                            # Specify url of the web page, here: url 
                                            source = urlopen(url).read()
                                            # Make a soup 
                                            soup = BeautifulSoup(source,'lxml')
                                            # Extract the plain text content from paragraphs
                                            text = ''
                                            for paragraph in soup.find_all('p'):
                                                text += paragraph.text
                                            # Clean text
                                            text = re.sub(r'\[.*?\]+', '', text)
                                            text = text.replace('\n', '')
                                            # get title of the wikipedia article
                                            page_title = soup.find_all('title')[0].text[:-12]
                                            file = open(working_dir + "Raw_TXT_Downloads/"+(str(crawled_count+1))+") "+name+".txt","w", encoding='utf-8')
                                            file.write(url + '\n' + page_title + '\n' + text)
                                            file.close()

                                            extracted_urls.append(url)
                                            crawled_count+=1
                                            focused_crawler_log.write(str(crawled_count)+") "+url+"\n")
                                            print(str(crawled_count)+") "+url)

                        else:
                            # limit of 1000 URLs reached
                            flag = False
                            print("Limit of 1000 URLs reached")
                            max_depth = depth
                            break

                    # Copy all the URLs from Frontier to Seen
                    seen_urls.append(frontier_url)

            # Case when no URLs found on the depth
            if len(extracted_urls) == 0:
                print("No matching URLs at Depth "+str(depth)+"\n")
                focused_crawler_log.write("No matching URLs at Depth "+str(depth)+"\n\n")
                flag = False
                max_depth = depth
                break
            # Copy all the Extracted URLs to the Frontier
            frontier_urls = extracted_urls
            focused_crawler_log.write("\n")

    # Maximum depth of Depth 3 reached        
    if flag:
        print(f"Searched till max depth {crawl_depth}")
        max_depth = crawl_depth

    focused_crawler_log.write("------------------------------------------------------------------------------------\n")
    focused_crawler_log.write("Logistics :\n\n")
    focused_crawler_log.write("Number of matching searches : "+str(crawled_count)+"\n")
    focused_crawler_log.write("Maximum depth reached : Depth "+str(max_depth)+"\n")
    focused_crawler_log.close()

seed_url = 'https://en.wikipedia.org/wiki/Health'
crawl_depth = 3
keyword = 'health'
spider(seed_url, keyword, crawl_depth)
