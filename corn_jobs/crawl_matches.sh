#!/bin/sh
# &> "/var/www/html/test/Adfsd/Tewre/thomas/corn_jobs/logs/log_${datetime}.txt"
#datetime=$(date '+%m_%d_%Y_%H_%M_%S')
# go to the spider directory
cd /var/www/webixhub/www/scrapers/boldtv
# run the spider
scrapy crawl boldtvnew
