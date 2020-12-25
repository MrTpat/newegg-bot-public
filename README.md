# Newegg Purchasing Bot - Public

#### For issues, please include your log file which is in the logs directory

## USAGE
1) Ensure python3, pipenv, and the latest Chrome version are installed
2) `git clone` the repository and enter it
3) Run `pipenv install` to install the virtual environment
4) Run `pipenv shell` to activate the virtual environment
5) Run `python gen_cookie.py` to generate cookies
	- This will open up a browser window
	- Login into newegg. Once logged in, wait for the page to completely stop loading.
	- In the Python shell prompt, click any button to save your cookies
	- You can click CTRL-C on the prompt to exit. Also exit out of the opened browser window.
	
6) Copy or move all json files in `configs-default/` to `configs/`
7) Edit the `configs/billing_config.json` file. This should match with your default Newegg card. Follow the format specified exactly.
8) Edit the `configs/jobs_config.json` file. Add more jobs to the array as you wish. All the jobs in this file will be run concurrently when the script is launched, so be careful about adding too many. Make sure each entry has a different job id. The attempts attribute is how many times to run that job before it is officially marked as a failed job. For provider, we are aware of the following possible entries: Discover, Visa, Mastercard
9) Edit the `configs/product_config.json` file.
	- If you are using combos, set `is_combo` to **true**. For combos, the URL of the newegg page looks like this: https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4212056. The p_id is the portion after Combo., so in this case it would be "4212056". The s_id is the p_id of the highest-value product in the combo. In this case the p_id of the Intel CPU. Read the next bullet point for info on how to get this.
	- If you are not using a combo, set `is_combo` to **false**. For single items, the URL looks like this: https://www.newegg.com/amd-ryzen-5-5600x/p/N82E16819113666. The p_id is the last portion, so in this case, it is N82E16819113666. The s_id is the last 8 digits of the p_id, hyphenated. In this case the s_id would be 19-113-666.
10) Edit the configs/settings_config file. The act_limit is how many attempts to try to ATC before failing. Similar for the other _limit variables. The timeout variable is the timeout for each request. If a request exceeds that time (in seconds) then it will fail. The cookie_file is the name of the cookie file you would like to use. Unless you manually changed this, it should stay as cookies.json.
11) Now, you can run the program. I recommend only running when there is a drop coming. For example, if there is a drop at 7 PM, generate your cookies at 6:55 PM. Then, run the actual script(described after this) at exactly 7 PM. The reason you need to generate fresh cookies is because they expire after an hour, so the ones you have on while may not work.
12) To run the script in test mode (all steps are completed except for order submission), run `python cli.py jobs_config_file.json --test`. To run the script in real mode, run `python cli.py jobs_config_file.json --real`. Feel free to make different job configurations for both your test and real modes. Running with no test or real parameter will default the program to test mode.
13) The script will provide output on what it is doing once you run it.
