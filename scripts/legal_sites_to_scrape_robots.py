"""
This script checks the robots.txt file of a list of Indian restaurant websites to determine if they allow web scraping.
It uses the `RobotFileParser` from the `urllib` library to parse the robots.txt file and check if scraping is allowed for the homepage of each website.

Helps find out which restaurant websites can be scraped legally faster.

After the response, manual verification is needed to verify extra parameters like:
1. The item URL can be scraped as per robots.txt or not.
2. Metadata likes prices etc are present or not!
"""

from urllib.robotparser import RobotFileParser

# List of restaurant/aggregator websites to check (a lot more can be added)
restaurant_websites = [
    "https://www.zomato.com",
    "https://www.swiggy.com",
    "https://www.dominos.co.in",
    "https://www.burgerking.in",
    "https://www.barbequenation.com",
    "https://www.pizzahut.co.in",
    "https://www.faasos.com",
    "https://www.eatsure.com",
    "https://www.mcdelivery.co.in",
    "https://www.kfc.co.in",
    "https://www.subway.com/en-IN",
    "https://www.haldirams.com",
    "https://www.behrouzbiryani.com",
    "https://www.box8.in",
    "https://www.freshmenu.com",
    "https://www.mojoPizza.in",
    "https://www.biryaniByKilo.com",
    "https://www.ovenstory.in",
    "https://www.naturalsicecreams.in",
    "https://www.creambell.com",
    "https://www.chaayos.com",
    "https://www.cafecoffeeday.com",
    "https://www.starbucks.in",
    "https://www.punjabgrill.in",
    "https://www.smokinjoespizza.in",
    "https://www.tacobell.co.in",
    "https://www.cinnabon.in",
    "https://www.carlscafe.in",
    "https://www.kailashparbat.com",
    "https://www.sagarratna.in",
    "https://www.bikano.com",
    "https://www.annapurnafoods.in",
    "https://www.nandhinirestaurant.com",
    "https://www.theobroma.in",
    "https://www.jumboking.co.in",
    "https://www.idfreshfood.com",
    "https://www.biryani.me",
    "https://www.theyellowchillis.com",
    "https://www.kaffedelhi.com",
    "https://www.nalandarestaurant.in",
    "https://www.nirulas.com",
    "https://www.angarebiryani.com",
    "https://www.thebiryaniinc.com",
    "https://www.biggiesburger.com",
    "https://www.wowmomo.com",
    "https://www.freshpressery.com",
    "https://www.tibbsfrankie.com",
    "https://www.thegoodbowl.in",
    "https://www.hangoutcakes.com",
]


def check_scrapability(websites, user_agent="*"):
    results = []

    for site in websites:
        robots_url = site.rstrip("/") + "/robots.txt"
        rp = RobotFileParser()
        try:
            rp.set_url(robots_url)
            rp.read()

            # Let's check if we can scrape the homepage
            test_path = site.rstrip("/") + "/"
            can_fetch = rp.can_fetch(user_agent, test_path)
            results.append((site, can_fetch))
        except Exception as e:
            results.append((site, f"Error: {e}"))

    return results


# Run and print results
results = check_scrapability(restaurant_websites)

for site, status in results:
    print(
        f"{site} --> {'Allowed' if status is True else 'Disallowed' if status is False else status}"
    )

"""
RUN OUTPUT




resturant_chat on  main [?] is 📦 v0.1.0 via 🐍 v3.13.3 
❯ uv run python ./utils/robots_parser.py 
https://www.zomato.com --> Disallowed
https://www.swiggy.com --> Disallowed
https://www.dominos.co.in --> Allowed
https://www.burgerking.in --> Allowed
https://www.barbequenation.com --> Disallowed
https://www.pizzahut.co.in --> Allowed
https://www.faasos.com --> Disallowed
https://www.eatsure.com --> Disallowed
https://www.mcdelivery.co.in --> Allowed
https://www.kfc.co.in --> Error: <urlopen error [Errno 111] Connection refused>
https://www.subway.com/en-IN --> Allowed
https://www.haldirams.com --> Error: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte
https://www.behrouzbiryani.com --> Disallowed
https://www.box8.in --> Allowed
https://www.freshmenu.com --> Allowed
https://www.mojoPizza.in --> Allowed
https://www.biryaniByKilo.com --> Allowed
https://www.ovenstory.in --> Disallowed
https://www.naturalsicecreams.in --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.creambell.com --> Allowed
https://www.chaayos.com --> Allowed
https://www.cafecoffeeday.com --> Error: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)>
https://www.starbucks.in --> Allowed
https://www.punjabgrill.in --> Allowed
https://www.smokinjoespizza.in --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.tacobell.co.in --> Disallowed
https://www.cinnabon.in --> Error: <urlopen error [Errno 110] Connection timed out>
https://www.carlscafe.in --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.kailashparbat.com --> Allowed
https://www.sagarratna.in --> Allowed
https://www.bikano.com --> Allowed
https://www.annapurnafoods.in --> Error: <urlopen error [Errno 110] Connection timed out>
https://www.nandhinirestaurant.com --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.theobroma.in --> Allowed
https://www.jumboking.co.in --> Allowed
https://www.idfreshfood.com --> Allowed
https://www.biryani.me --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.theyellowchillis.com --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.kaffedelhi.com --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.nalandarestaurant.in --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.nirulas.com --> Allowed
https://www.angarebiryani.com --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.thebiryaniinc.com --> Error: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1000)>
https://www.biggiesburger.com --> Allowed
https://www.wowmomo.com --> Allowed
https://www.freshpressery.com --> Allowed
https://www.tibbsfrankie.com --> Allowed
https://www.thegoodbowl.in --> Error: <urlopen error [Errno -2] Name or service not known>
https://www.hangoutcakes.com --> Disallowed
"""
