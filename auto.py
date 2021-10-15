from requests_html import HTMLSession
import time
import datetime

s = HTMLSession()


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'ncbi_sid=324F04060EA7D083_9471SID; _ga=GA1.2.2054965354.1625982931; pmc.article.report=; pmc_labs_version=""; _gid=GA1.2.732976300.1633866554; WebEnv=1ncJSF8xxGLn_nGzKWJq-Ojyv_hBiRcSAQi8bQV-YEWQd%40324F04060EA7D083_9471SID; _gat_ncbiSg=1; QSI_SI_4ZW5tSQNmEIzIvY_intercept=true; _gat_dap=1; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgCIAYBC2AzAKwCCAnBUUfgOwCMDJuruRAYnUQGwAsuOuwYAmAHQMxAWzgiQAGhABXAHYAbAPYBDVCqgAPAC6ZQcrGCkBjALQAzCBpWGoK9IqKZwVhSD6etEIbIlmpQPiSePiK4nniEpJTUtIzMbOxcvAJCRKIS0rJRDJ4WNvaOzq4YJRgBQSFQGAByAPKNAKJRZiAA7r1iKpYARsj9alL9yIhiAOYaMFEUngy8PD5EMVh0PAAca0VYyzyr7l10IrvuHli2WmoAzmHufliGEEqPIES7WGuLWHwkCgkC6+Da+bY7GKKPhXEC4MQ5CQ+PjPZTqbS6AzGaERLBQkAkWHbPhFRQkVEkHbhVabbYgkh0Tz4nj7EA8IEgAC+nKAA===',
    'referer':'https://www.ncbi.nlm.nih.gov/labs/pmc',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'connection':'keep-alive'
}

print('starting to extract...')
start_time = datetime.datetime.now() 
input_file = open('inputfile.txt', 'r')
urls = input_file.readlines()
for url in urls:
    urllist = url.strip()
    try:
        r = s.get(urllist, headers=headers)
        pdfs = r.html.find('#main-content > aside > section:nth-child(1) > ul > li.pdf-link.other_item')
        for item in pdfs:
            pmcpdf = 'https://www.ncbi.nlm.nih.gov' + item.find('a', first=True).attrs['href']
            pmcid = item.find('a', first=True).attrs['href'].split('/')[-3]
            with open (pmcid + '.pdf', 'wb') as f:
                res = s.get(pmcpdf, stream=True)
                for chunk in res.iter_content(2000):
                    f.write(chunk)        
            time.sleep(3)
            f.close()  
            
    except ConnectionError:
        pass