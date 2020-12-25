# Newegg Purchasing Bot - Public

#### For issues, please include your log file which is in the logs directory

## USAGE
1) Ensure python3, pipenv, and the latest Chrome version are installed.
2) `git clone` the repository and enter it.
3) Run `pipenv install` to install the virtual environment.
4) Run `pipenv shell` to activate the virtual environment.
5) Run `python gen_cookie.py` to generate cookies.
	- This will open up a browser window.
	- Login into Newegg. Once logged in, wait for the page to completely stop loading.
	- In the Python shell prompt, click any button to save your cookies.
	
6) Copy or move all json files in `configs-default/` to `configs/`.
7) Edit the `configs/billing_config.json` file. This should match with your default Newegg card. Follow the format specified exactly. For `card_provider`, we have confirmed the following possible entries: Mastercard, Visa, Discover, AmericanExpress
8) Edit the `configs/jobs_config.json` file. Add more jobs to the array as you wish. All the jobs in this file will be run concurrently when the script is launched, so be careful about adding too many. Make sure each entry has a different job name. The `attempts` attribute is how many times to run that job before it is officially marked as a failed job.
9) Edit the `configs/product_config.json` file.
	- If you are using combos, set `is_combo` to **true**. For combos, the URL of the Newegg page looks like this: https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4212056. The `p_id` is the portion after _Combo._, so in this case it would be _4212056_. The `s_id` is the `p_id` of the highest-value product in the combo; in this case, the `p_id` of the Intel CPU. Read the next bullet point for info on how to get this.
	- If you are not using a combo, set `is_combo` to **false**. For single items, the URL looks like this: https://www.newegg.com/amd-ryzen-5-5600x/p/N82E16819113666. The `p_id` is the last portion, so in this case, it is _N82E16819113666_. The `s_id` is the last 8 digits of the `p_id`, hyphenated. In this case the `s_id` would be _19-113-666_.
10) Edit the `configs/settings_config.json` file. The `atc_limit` is how many attempts to try to add to cart before failing. Similar for the other _limit variables. The timeout variable is the timeout for each request. If a request exceeds that time (in seconds) then it will fail. The `cookie_file` is the name of the cookie file you would like to use. Unless you manually changed this, it should stay as `cookies.json`.
11) Now, you can run the program. I recommend only running when there is a drop coming. For example, if there is a drop at 7 PM, generate your cookies at 6:55 PM. Then, run the actual script (described in the next step) at exactly 7 PM. The reason you need to generate fresh cookies is because they expire after an hour.
12) To run the script in **test mode** (all steps are completed except for order submission), run `python cli.py jobs_config.json --test`. To run the script in **real mode** (order is actually submitted), run `python cli.py jobs_config.json --real`. Feel free to make different job configurations for both your test and real modes. Running with no parameter will default the program to test mode.
13) The script will provide output on what it is doing once you run it.
