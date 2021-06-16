# SCRYPTO

## What ?
Crypto currencies scraping

(At the moment, only bitcoin and ethereum crypto currencies are supported)

## How ?
A python script is running in a container, and scrape informations (using CoinGecko API) about crypto currencies. Then this informations are send to a SQL database.</br>
(You can also run the script alone with a .env file and a systemd service)
</br>

# SETUP
- You can launch this scraper by simply using the "docker-compose.yml" file that i let you on this repo.

## Docker-compose file
Here is an example of docker-compose file.

```
version: "3"
services:
  scrypto:
    image: baldurr/scrypto:latest
    container_name: scrypto
    environment:
      - CRYPTO_LIST=bitcoin,ethereum
      - DEVISE_1=eur
      - DEVISE_2=usd
      - SCRAPE_TIME=300
      - SQL_USER=root2
      - SQL_PASSWORD=mypwd
      - SQL_HOST=192.168.1.20
      - SQL_DB=db_scrypto
      - SQL_PORT=3308
    restart: unless-stopped
```

## Environment variable

List of all currencies available:</br>
  "btc",
  "eth",
  "ltc",
  "bch",
  "bnb",
  "eos",
  "xrp",
  "xlm",
  "link",
  "dot",
  "yfi",
  "usd",
  "aed",
  "ars",
  "aud",
  "bdt",
  "bhd",
  "bmd",
  "brl",
  "cad",
  "chf",
  "clp",
  "cny",
  "czk",
  "dkk",
  "eur",
  "gbp",
  "hkd",
  "huf",
  "idr",
  "ils",
  "inr",
  "jpy",
  "krw",
  "kwd",
  "lkr",
  "mmk",
  "mxn",
  "myr",
  "ngn",
  "nok",
  "nzd",
  "php",
  "pkr",
  "pln",
  "rub",
  "sar",
  "sek",
  "sgd",
  "thb",
  "try",
  "twd",
  "uah",
  "vef",
  "vnd",
  "zar",
  "xdr",
  "xag",
  "xau",
  "bits",
  "sats"
</br>
  
| Var         | Usage | Info |
|-------------|-------|------|
| CRYPTO_LIST | List of currencies separated by ','    | Max: 2 currencies    |
| DEVISE_1    | Name of the 1st currencie defined      |   ex: eur   |
| DEVISE_2    | Name of the 1nd currencie defined    |     ex: usd |
| SCRAPE_TIME    | Scrape interval in second  |  ex: 300 = 5min    |
| SQL_USER    | SQL user used  |      |   |   |
| SQL_PASSWORD    | SQL user password   |      |   |   |
| SQL_HOST    | SQL host which host the database  |  ex: 192.168.1.20, don't set localhost while this will refer to the scrypto container if you use the docker method|
| SQL_DB    |   SQL database name   | This var must be set to 'db_scrypto'    |
| SQL_PORT    |  SQL database port     |      |



## Insatallation

### SQL configuration
To use correctly this image, you must create a database named 'db_scrypto'.

If you use the docker method, connect to the scrypto container:
```
docker exec -it scrypto /bin/bash
```

Then connect to the SQL database:
```
mysql -u myuser -p
```

Enter your password and display databases like this:
```
SHOW databases;
```
If 'db_scrypto' doesn't exist, create it:
```
CREATE DATABASE db_scrypto;
```

Then you have to create the tables to store the data.</br>
NOTICE: </br>
- For the table name, please name it like the crypto currencie name: bitcoin, ethereum
- For the value columns, set the name of the column like this: value_mycurrencie (ex: value_usd)

```
CREATE TABLE bitcoin (data_id INT NOT NULL AUTO_INCREMENT,time DATETIME, metric VARCHAR(20),value_eur VARCHAR(20),value_usd VARCHAR(20), PRIMARY KEY (data_id));
CREATE TABLE ethereum (data_id INT NOT NULL AUTO_INCREMENT,time DATETIME, metric VARCHAR(20),value_eur VARCHAR(20),value_usd VARCHAR(20), PRIMARY KEY (data_id));
```

Now you are ready to collect data
</br>

### Docker configuration
```
mkdir scrypto
cd scrypto
wget https://raw.githubusercontent.com/Baldurrr/scrypto/main/docker-compose.yml
docker-compose up -d

Wait a bit and:
docker logs scrypto (will display the api response if the configuration worked)
```

</br>

## THE RESULT
Grafana dashboard example:
![image](https://user-images.githubusercontent.com/77190420/122207393-60dc3480-cea2-11eb-86e9-2a731e26809b.png)

