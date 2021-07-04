# Torrent Search

| Tested version | PyPi package | Drone CI | Travis CI |
|:--------|:------|:------|:------------|
| [![PyVersion](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) | ![PyPI](https://img.shields.io/pypi/v/torrentSearch) | [![Build Status](https://drone.schleppe.cloud/api/badges/KevinMidboe/torrent_search/status.svg)](https://drone.schleppe.cloud/KevinMidboe/torrent_search) | [![Build Status](https://travis-ci.org/KevinMidboe/torrent_search.svg?branch=master)](https://travis-ci.org/KevinMidboe/torrent_search)

| Code coverage | Known vulnerabilities | License |
|:--------|:------|:------------|
| [![codecov](https://codecov.io/gh/KevinMidboe/torrent_search/branch/master/graph/badge.svg)](https://codecov.io/gh/KevinMidboe/torrent_search) | [![Known Vulnerabilities](https://snyk.io/test/github/kevinmidboe/torrent_search/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/kevinmidboe/torrent_search?targetFile=requirements.txt) | [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

## Idea
The idea behind this project is to create a modular torrent searcher/indexer in python. Currently we have the option to search for two sites, thepiratebay and with jackett. To add more sites one only needs to create a scraper script for a specific service, and from there create torrent class objects that are returned back to the search script. If the new site needs specific configuration values this can be set in the config.ini file and needs to be imported in the site selector in search.py. 

If you have a site you want to add support to please contact me or fork this repository and create a pull request! If there are any other questions please don't hesitate to ask or add to this project.

## Table of Contents

* [Setup a Virtual Environment](#setup_a_virtual_environment)
  * [Installation](#env_installation)
  * [Usage](#env_usage)
* [Configure the Config File](#configure_config_file)
* [Install Required Dependencies](#install_requirements)
* [Usage](#usage)
  * [Running](#usage_running)
  * [Changing the Default Search Site](#changing_default)

<a name='setup_a_virtual_enviroment'></a>
## Setup a Virtual Environment
The reason for setting up a virtual environment is primarily based on two reasons. Firstly when in a virtual environment we don't use tha pacekages already installed on your machine. This means that if our project uses a python package say *django* we can have our virtual environment use a specific version of it that we know works with our project, and not the global one installed on your user that may be incompatible version of django that introduces unexpected behaviour in your project. The second reason is to limit the number of packages we install on the machine. This is not strictly a specific features used for this project, but it's good to get in the habit of for better control over your projects. Say we delete this project at a later date, then we will take with us all the python packages we have installed with pip. On the contrary if we have installed the required python packages globaly (that is outside a virtual environment), the packages installed would remain on your machine without getting removed when no longer in use by a project. This could case problems at a later time when trying to use a maybe outdated package.

<a name='env_installation'></a>
### Installation
To install virtualenv, simply run:  

```
 $ pip install virutalenv
```

<a name='env_usage'></a>
### Usage
After you have downloaded this project go to it in your terminal by going to the folder you downloaded and typing the following:


```
 $ cd torrentSearch/
```

The to setup a virtual environment enter this:

```
 $ virtualenv -p python3.6 env
```

 > If you get an error now it might be because you don't have python3.6, please make sure you have python version 3.6 if else you can download it from [here](https://www.python.org/downloads/)


First we navigate to the folder we downloaded.

Then we use the ```virtualenv``` command to create a ```env``` subdirectory in our project. This is where pip will download everything to and where we can add other specific python versions. Then we need to *activate* our virtual environment by doing:

```
 $ source env/bin/activate
```

You should now see a ```(env)``` appear at the beginning of your terminal prompt indicating that you are working from within the virtual environment. Now when you install something: 

```
 $ pip install <package>
```

It will get installed in the env folder, and not globaly on our machine. 

The leave our virtual environment run: 

```
 $ deactivate
```

<a name='configure_config_file'></a>
## Configure the Config File
The default site the is queried is thepiratebay, but this is a manual scrape of the webpage. The real power to this project is to setup [jackett](#https://github.com/Jackett/Jackett). Jackett works as a proxy server: it translates queries from apps into tracker-site-specific http queries, parses the html response, then sends results back to the requesting software. This allows for getting recent uploads (like RSS) and performing searches. Jackett is a single repository of maintained indexer scraping & translation logic - removing the burden from other apps.  
It is highly encoraged to install and run jackett locally. It is not a resource heavy program and the guide on their github page is well written and easy to follow. 

Now you can add all the indexers you want in one place and our searcher will pull from this list and return it to us. 

The following is where we need to do some manual editing of our config file. Open to ```config.ini``` in your favorite text editor. 

``` 
 $ (vi) config.ini
```

Then you need to change the HOST and APIKEY to reflect the values in your jackett application. When this is done we can use jackett to search for our torrents from multiple indexers. You can change the site your search from with the ```-s``` arguement when running this script.

To change to default search site follow the instructions [Usage : Changing the Default Search Site](#changing_default)

<a name='install_requirements'></a>
## Install Required Dependencies
Now that we have our virutalenv set up and activated we want to install all the necessary files for using our torrent searcher. To install it's dependencies do the following:

```
 $ pip install -r requirements.txt
```

Now we have our neccessary packages installed!


<a name='usage'></a>
## Usage
<a name='usage_running'></a>
### Running
To run search the available indexers run the following:

```
 $ ./torrentSearch/search.py -s [SITE (default:piratebay)]] query
```

This is also explained by typing:

```
 $ ./torrentSearch/search.py -h (--help)
```

<a name='changing_default'></a>
### Changing the Default Search Site
To change to default search site to *jackett* run the following:

```
torrentSearch/./search.py -s DEFAULT jackett
```
