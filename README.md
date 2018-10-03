# py-facebook-webhook
[![Python 3.5+](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build](https://travis-ci.org/yc0/py-facebook-webhook.svg?branch=master)](https://travis-ci.org/yc0/py-facebook-webhook)

A basic scaffold for high performance Facebook messenger bot in Sanic : Async web server that's written to go fast

Sanic is very **high performance** JSON serialization, so it is very suitable for facebook webhook. Please refer the benchmark and related test source codes 
[Techempower](https://www.techempower.com/benchmarks/#section=data-r15&hw=ph&test=json)

## Key Features

- uvloop : which is a fast, drop-in replacement of the built-in asyncio event loop. uvloop is implemented in **Cython** and uses libuv under the hood.
- aiohttp : which is an HTTP client/server for **asyncio**.
- webhook
- facebook

## Get Started

Steps to get up and running:

- Create a new facebook App .https://developers.facebook.com/quickstarts/?platform=web

- Create a new facebook Page https://www.facebook.com/pages/create

- Go to your app and to the messengers tab on the sidebar

- Generate a token for your page. 

- Edit your webhook configuration

  ![](img/app-setup.png)
  ![](img/edit-subscription.png)
  
  Verify Token is any string you like to help your webhook app confirm or authenticate the source.

## Run your webhook

I adopt environment variables to inject the PAGE_TOKEN and VERIFY_TOKEN for security, and easy to port on the docker environment.


```
$ pip install -r requirment.txt
$ VERIFY_TOKEN=<your verfiy token> PAGE_ACCESS_TOKEN=<your page token> python -m app.py 
```

the module support 5 parameters for non web server like gunicorn or nginx. Since the webhook in Facebook needs SSL, you must run with CERT.

```
--host 
-p, --port the app running port.
-d, --debug enable debug mode.
--cert, put your cert, 
--key, your cert passphrase.
```


## benchmark
https://blog.signifai.io/not-your-fathers-python-amazing-powerful-frameworks/

## local test
While you try to test a webhook on your own circumstance, you might encounter callback issues.
Callback function always needs two requirements:

- Domain name
- SSL (HTTPS)

The testing procedure would like this.
1. coding on the local site, and debuging with experience.
2. upload toward server
3. On your chatbot platform, check if the req-ack work well
4. Check log message on server
5. If there's an error, go back to step 1

Ngrok is an antidote for this situation.
It provides localhost toward https with domain name
such as localhost:5000 to https://bbcc3.ngrok.com

you can go visiting [https://ngrok.com/](https://ngrok.com/), and check how you can exploit it well.
