# Take that Zendesk ticket

Have you managed to embarass yourself repeatedly in front of your superiors
because you keep forgetting to click `Submit` after you clicked `take-it` on a Zendesk ticket?
This piece of code will make sure you
properly take that ZD ticket and you don't forget to press submit,
as it does that all for you!

## TL;DR

1. Install the `selenium` python module if you don't have it already.
   Either from your package manager like `sudo apt install python3-selenium`,
   or if you are OK with using `pip` then use the `requirements.txt`
   like `pip3 install --user -r requirements.txt`
1. Install the [browser driver](
https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/) for your browser.
1. Run the script and fill in the parameters:

````bash
./takeit.py

E-Mail:
> devXXXX@XXXXXXX.com
Password (will be hidden):
> XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Ticket URL:
> https://XXXX.zendesk.com/agent/tickets/XXXXX
````

### Dependencies

#### Installation of python dependencies

##### Ubuntu, Debian
````bash
sudo apt install python3-selenium`
````

#### RHEL, Fedora
````bash
sudo dnf install python3-selenium
````

#### pip

````bash
pip3 install -r requirements.txt
````

#### Webdriver for your browser
##### Chromium and Chromium based browsers (Chrome, Microsoft Edge, Opera, Brave)
https://chromedriver.chromium.org/downloads

##### Firefox and derivatives (Floorp, LibreWolf)
* https://github.com/mozilla/geckodriver/releases

##### Firefox in isolated environment

When using firefox, selenium passes only a base64 encoded profile to the geckodriver
in a call, so on the caller side you can't controll where geckodriver puts that profile.
The geckodriver creates temporary profile directory with the user profile .js in it,
regardless of what you try to set in the selenium using python code.
That directory needs to be accessible to the firefox instance.
By default that temporary profile directory is determined by geckodriver
and can be influenced by environment variables as explained here:
https://firefox-source-docs.mozilla.org/testing/geckodriver/Profiles.html#default-locations-for-temporary-profiles
On Linux it is ${TMPDIR}, and if your firefox is an alias to 'docker run ... firefox'
or 'flatpak run ... firefox' then that temporary directory won't be available to the isolated/sandboxed
firefox. On flatpak the external /tmp is not even possible to access currently.
So in such cases consider a wrapper around geckodriver which sets ${TMPDIR}
to something that is availabe inside the docker, flatpak etc.
And also exists! Because geckodriver won't create that directory for you.
