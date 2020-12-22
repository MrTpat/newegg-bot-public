# newegg-bot-public

## THIS BOT CAN CHECKOUT OF NEWEGG IN <4 SECONDS.

## Currently, the interval limit I set is 30 seconds, since newegg bans liberally. To circumvent this, you can run python3 buyBot.py 5600X
## when you know a drop is coming. Run it ~30 seconds before the drop and you should be golden.

Usage:

Navigate to the repo, and run pipenv install. This will take some time.
When this is done, configure the config.ini file how you want. For notifications, make sure to fill the bottom most configuration.

Imagine we want to bot this product: https://www.newegg.com/amd-ryzen-5-5600x/p/N82E16819113666

The primary ID is the part following the /p/, so it is N82E16819113666.
The secondary ID is found by right-clicking the image in Chrome, inspecting, and copying the ID before the -V part. For example, for this html code of the picture:

```
<img alt="" id="mainSlide19-113-666" class="product-view-img-original" src="https://c1.neweggimages.com/ProductImage/19-113-666-V01.jpg">
```

The secondary ID is 19-113-666 (make sure to add dashes to the config).

## ALSO MAKE SURE TO UPDATE YOUR CREDENTIALS AT THE BOTTOM OF THE CONFIG SO THAT THEY MATCH WITH YOUR CARD INFO. THE INFO SHOULD BE TIED TO YOUR PRIMARY CARD IN NEWEGG.

## FOR COMBOS, THE PRIMARY ID IS THE THING AFTER COMBO. IN THE URL. THE SECONDARY ID IS THE PRIMARY ID OF THE HIGHEST-PRICED PRODUCT IN THE COMBO!!!

Once done with the config, run pipenv shell.

To run the scanner for an item, say the 5600X, I would do python scanner.py 5600X.
To run the buybot (you know a drop is coming), run python buyBot 5600X.

Running with no arguments will run the test configuration and will not actually purchase anything.
