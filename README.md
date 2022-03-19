# mobile-build-server
Builder server for Agregore Mobile (Chromium Android)

**IN PROGRESS**

## Plans

- Automate builds of chromium Android
- Specify repo and commit to use
- Patch over top of Chromium source
- Run android build
- Post APK somewhere (github releases? temporary location?)
- Reset the state of the chromium source
- Make it easy ish to self host on Digital Ocean droplets

## Details

- HTTP service modelled after the Kiwi Browser
- Use token authentication in the querystring
- Queue up requests

## Setup

Configure `git` with your username and email so that patches may be applied.

```
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```
