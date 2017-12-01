
# coding: utf-8

# In[10]:


import requests, bs4
url = "https://coinmarketcap.com/currencies/"

res = requests.get(url)

try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

soup = bs4.BeautifulSoup(res.text, "html5lib")      

data_rows = soup.findAll('tr')

currencies = []

for i in range(1, 101):
    currencies.append(data_rows[i].get('id')[3:])
    
#currencies


# In[15]:


import requests, bs4, os

for currency in currencies:

    url = "https://coinmarketcap.com/currencies/" + currency + "/historical-data/?start=20000428&end=20171012"

    res = requests.get(url)

    soup = bs4.BeautifulSoup(res.text, "html5lib")   
    data_rows = soup.findAll('tr')

    all_data = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    volumes = []
    market_caps = []


    for i in range(len(data_rows)):
        row = []
        datapoint = []

        # go through each data element in each table row
        for td in data_rows[i].findAll('td'):

            # get text and append to row
            row.append(td.getText())

        # add row to matricies
        if len(row) > 6:
            open_prices.append(float(str(row[1])))
            high_prices.append(float(str(row[2])))
            low_prices.append(float(str(row[3])))
            close_prices.append(float(str(row[4])))

            volume = list(str(row[5]))
            if volume[0] is "-":
                volume = str(all_data[i-1][4])
                volume = list(volume)

            volume = [char for char in volume if (char is not "," and char is not u",")]
            volume = "".join(volume)
            volumes.append(float(volume))

            cap = list(str(row[6]))
            if cap[0] == '-':
                cap = str(all_data[i-1][5])
                cap = list(cap)

            cap = [char for char in cap if (char is not "," and char is not u",")]
            cap = "".join(cap)
            market_caps.append(float(cap))

            datapoint.append(float(str(row[1])))
            datapoint.append(float(str(row[2])))
            datapoint.append(float(str(row[3])))
            datapoint.append(float(str(row[4])))
            datapoint.append(volume)
            datapoint.append(cap)
        all_data.append(datapoint)



    writefile = os.path.expanduser(currency+"_all_data"+".csv")
    writer = open(writefile, "w")
    writer.write("open, high, low, close, volume, cap")
    writer.write('\n')

    for line in all_data:
        temp = "" 
        for element in line:
            temp += str(element)
            temp += ','
        temp = temp[:-1]
        writer.write(temp)
        writer.write('\n')

    writer.close

    writefile = os.path.expanduser(currency+"_open"+".csv")
    writer = open(writefile, "w")
    for line in open_prices:
        writer.write(str(line))
        writer.write('\n')
    writer.close

    writefile = os.path.expanduser(currency+"_close"+".csv")
    writer = open(writefile, "w")
    for line in close_prices:
        writer.write(str(line))
        writer.write('\n')
    writer.close

    writefile = os.path.expanduser(currency+"_high"+".csv")
    writer = open(writefile, "w")
    for line in high_prices:
        writer.write(str(line))
        writer.write('\n')
    writer.close

    writefile = os.path.expanduser(currency+"_low"+".csv")
    writer = open(writefile, "w")
    for line in low_prices:
        writer.write(str(line))
        writer.write('\n')
    writer.close

    print("Scraped", currency)


# In[ ]:




