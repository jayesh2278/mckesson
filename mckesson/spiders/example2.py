import scrapy
import pandas as pd
import json

class Example2Spider(scrapy.Spider):
    name = "example2"
    df = pd.read_csv("remain_products.csv")

    def start_requests(self):
        for index, row in self.df.iterrows():
            manufc_name = row['ManufacturerName']
            manufac_itemcode = row['ManufacturerItemCode']
            print("______________________",manufac_itemcode)
            url = f"https://liveapi.yext.com/v2/accounts/2012431/answers/query?api_key=54d95e3acf60def2fb1e2b5acadab75f&v=20180204&experienceKey=mckesson-answers&input={manufc_name}%20{manufac_itemcode}&version=PRODUCTION&locale=en&referrerPageUrl=https%3A%2F%2Fwww.google.com%2F"
            headers = {
                        'authority': 'liveapi.yext.com',
                        'accept': '*/*',
                        'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8,gu;q=0.7',
                        'dnt': '1',
                        'origin': 'https://www.mckesson.com',
                        'referer': 'https://www.mckesson.com/',
                        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'cross-site',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        # 'Cookie': 'session-id=80751ffb-00b6-4326-a53f-aa851aae4bf0; __cf_bm=idOaFDKa4eHsxwB_U4USZ7LXotXMDm26Of7U6jRcDa8-1704816690-1-AfTyXXXeDPx0bgoxhAj8XnGng8cShHCvbmV07MS3pz7319LtF9WtVhwEgZ86kXjaKo8GTvflY8rLuRZXGIzA23NXYm6t1NgyTVHiT6XiUsQN'
                    }
            yield scrapy.Request(url=url,headers=headers,meta={'manufac_itemcode':manufac_itemcode,'manufc_name':manufc_name },callback=self.parse)
            

    def parse(self, response):
        test_manufc_name = response.meta.get('manufc_name')
        test_manuf_itemcode = response.meta.get('manufac_itemcode')
        data = json.loads(response.text)

        modules = data.get('response').get('modules')
        for module in modules:  
            results = module.get("results")
            for result in results:
                itemnumber = result.get('data').get('c_productModelNumber')
                
                id = result.get('data').get("id")
                productName = result.get('data').get("c_productInvoiceTitle")
                description = result.get('data').get("name")

                manufacturer = result.get('data').get('c_productManufacturer')
                manufacturerID = result.get('data').get("c_productModelNumber")
                    
                images = result.get('data').get("c_productImage")
                features = result.get('data').get('c_productSpecificationsText')
                producturl = result.get('data').get('c_productURL')

                if (str(test_manuf_itemcode)==str(manufacturerID)):
                    print(f'MATCH________{test_manuf_itemcode} __and__ {manufacturerID}')

                    yield{
                            'Itemid':id,
                            'itemurl': producturl,
                            'ManufacturerID':manufacturerID,
                            'ManufacturerName':manufacturer,
                            'ProductName': productName,
                            'Description':description,
                            'Feature':features,
                            'Images': images      
                        }
                else:
                    print(f'not match________{test_manuf_itemcode} __and__ {manufacturerID}')    
            





