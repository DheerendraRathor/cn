# IIT Bombay Community Network

Community Network for IIT Bombay

## Setup (Before Installation)
- Follow all steps mentioned in `INSTALLATION.md`
- Edit `iitbcn/settings/conf.sample.py` to `iitbcn/settings/conf.py`

## Setting up local machine for development
- Use Python 3.5
- Install and configure virtualenvwrapper https://virtualenvwrapper.readthedocs.org/en/latest/
- In local machine use `pip install -r requirements/local.txt`
- Edit `iitbcn/settings/conf.py` to your local settings

## Setting up Production server
- Use Python 3.5
- Install and configure virtualenvwrapper https://virtualenvwrapper.readthedocs.org/en/latest/
- In local machine use `pip install -r requirements/production.txt`
- Edit `iitbcn/settings/conf.py` to add your production level settings
- Set environment variable `DJANGO_SETTINGS_MODULE` to `iitbcn.settings.production`
- Continue with Django deployment normally
