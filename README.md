FastSFC
======================

FastSFC is a search engine for listed company documents. We currently support documents on HKSE, NYSE, NASDAQ and AMEX. Website: http://fastsfc.com

## Dependencies

FastSFC's webapp runs on Django, React and MySQL. You will need the following dependencies in order to set it up:

* python 3.6.5
* pip 19.1.1
* node 10.15.1
* npm 6.9.0
* npm-run-all 4.1.5
* mysql 5.7.23

## Deployment structure

FastSFC is deployed with the following servers:

1. DB server: MySQL hosted on Amazon RDS
2. Search DB server: ElasticSearch hosted on ElasticCloud
3. Web server: React client and Django server (i.e. code in this repo) hosted on EC2
4. Compute server: Scraper code (i.e. code in scraper repo) hosted on EC2 that runs periodic cron jobs to fetch companies and documents

Web and compute servers are Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-1035-aws x86_64).

## Setup

**Create virtualenv for project**
```
pip install virtualenv
virtualenv env
source env/bin/activate
```

**Clone repository, install packages and configure settings**
```
cd path/to/app/repository
pip3 install -r requirements.pip
cp app/settings/local.sample.py app/settings/local.py
```

For errors installing `mysqlclient`, please refer to the package [docs](https://github.com/PyMySQL/mysqlclient-python). On macOS, you may have to:

1. Install MySQL development headers and libraries: `brew install mysql-connector-c`
2. Fix bug on MySQL Connector/C

```
which mysql_config
vim path/to/mysql_config
```

On macOS, on or about line 112, change:

```
# Create options
libs="-L$pkglibdir"
libs="$libs -l "
```

to

```
# Create options
libs="-L$pkglibdir"
libs="$libs -lmysqlclient -lssl -lcrypto"
```

3. Configure SSL by adding exports suggested in `brew info openssl` to `~/.bash_profile`

**Create and prepare MySQL database**
Ensure DATABASES in app/settings/local.py is configured to connect to MySQL database
```
mysql -u {{ mysql_user }}
create database {{ db_name }}
exit
```

** Seed database**

Download and install seed database from [url](https://drive.google.com/open?id=1nj9MKAMwonmMhQj92TZR0-VN_abCitQ5). (will take a while as database is 1.5GB)

Migrate to update table structure.
```
python3 manage.py migrate
```

**Install frontend dependencies**
```
npm install
```

**Start project**
```
npm run-script start
```

## Deployment
```
npm run-script deploy:web
npm run-script deploy:compute
```

## Scraper (Optional)

FastSFC is comprised of a webapp (django) and scraper (scrapy). If you have access to the scraper module and would like to use it with the webapp, you may clone it as follows:

```
git clone https://justinyek@bitbucket.org/justinyek/fast-crawler.git scraper
```