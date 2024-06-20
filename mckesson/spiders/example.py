import scrapy
import pandas as pd
import json

class ExampleSpider(scrapy.Spider):
    name = "mckesson"
    
    df = pd.read_excel("NDC.xlsx")
    
    def start_requests(self):
        for index, row in self.df.iterrows():
            manufc_name = row['ManufacturerName']
            manufac_itemcode = row['ManufacturerItemCode']
            url = f'https://mms.mckesson.com/suggest?query={manufc_name}%20{manufac_itemcode}'
            yield scrapy.Request(url,meta={'manufac_itemcode':manufac_itemcode}, callback=self.parse)

    def parse(self, response):
        test_manuf_itemcode = response.meta.get('manufac_itemcode')
        # test_manuf_name = response.meta.get('manufc_name')
        data = json.loads(response.text)
        productList =  data.get('productList')

        if productList is not None:
            for i in productList:
                itemid = i.get('id')
                manufacturerID = i.get('mfrId')
                manufacturerName = i.get('mfrName')
                description = i.get('description')
                invoice = i.get('invoice')

                features = i.get('features')
                features = ','.join(features)

                image_urls = i.get("images")
                base_url = 'https://imgcdn.mckesson.com/CumulusWeb/Images/Original_Image/'
                full_urls = [base_url + i_url for i_url in image_urls]
                images = ','.join(full_urls)

                popularity = i.get('popularity')
                productname = i.get('productName')

                seotext = i.get('seoTextHyphenated')

                if (str(test_manuf_itemcode)==str(manufacturerID)):
                    print(f'MATCH________{test_manuf_itemcode} __and__ {manufacturerID}')    
                    yield{
                        'Itemid':itemid,
                        'SeoText':seotext,
                        'ManufacturerID':manufacturerID,
                        'ManufacturerName':manufacturerName,
                        'ProductName': productname,
                        'Description':description,
                        # 'Invoice':invoice,
                        'Feature':features,
                        'Images': images,
                        # 'Popularity':popularity                
                    }
                else:
                    print(f'not match________{test_manuf_itemcode} __and__ {manufacturerID}')

        
    
