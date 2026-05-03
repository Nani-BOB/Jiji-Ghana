import requests

from bs4 import BeautifulSoup as bs4

import pandas as pd

ses = requests.Session()

ses.headers.clear()

my_headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    }

ses.headers.update(my_headers)

url = "https://jiji.com.gh/mobile-phones"

response = ses.get(url, timeout=10)

record = []


if response.ok:
   refined = bs4(response.content,"html.parser")
   
   mobile_phone_data = refined.find_all("div", {"class":"masonry-item"})
       
   for mobile_phone in mobile_phone_data:
           
            name_data = mobile_phone.find("div",{"class":"b-advert-title-inner qa-advert-title b-advert-title-inner--div"})
        
            if name_data is None:
                
                continue
                
            else:
                
                human_name_data = name_data.text.strip()
            
                #name_list.append(human_name_data)
            
                price_data = mobile_phone.find("div",{"class":"qa-advert-price"})
                    
                if price_data is None:
                     human_price_data = "N/A"  
                    #price_list.append("N/A")
                        
                else:
                        
                    human_price_data = price_data.text.strip()
                    
                    #price_list.append(human_price_data)
                                        
                address_data = mobile_phone.find("span",{"class":"b-list-advert__region__text"})
                    
                if address_data is None:
                    human_address_data = "N/A"
                    #address_list.append('N/A')
                    
                else:
                        
                    human_address_data = address_data.text.strip()
                    
                    #address_list.append(human_address_data)
                
                url_listing_data = mobile_phone.find("a")
                    
                if url_listing_data is None:
                    link = "N/A"
                    #url_list.append("N/A")
                        
                else:
                    
                    link = url_listing_data.get("href", None)
                    
                    if link is None:
                        link = "N/A"
                        #url_list.append("N/A")
                    
                    else:
                        pass
                        #url_list.append(link)
                record.append({
                    "Name":human_name_data,
                    "Price":human_price_data,
                    "Address":human_address_data,
                    "URL":link
                            })
else:
    print(f'An error occured and a {response.status_code} was received')

'''record.append({
    "Phone Name":name_list,
    "Phone Price":price_list,
    "Address":address_list,
    "Listing URL":url_list,
    })'''

df = pd.DataFrame(record)

df.to_csv("Project_One.csv", index=False, encoding="utf-8-sig")

print("Done")