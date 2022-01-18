#!/bin/bash

scp ./*.* root@121.4.106.139:/var/www/html/Bidding/
scp -r ./Bidding/ root@121.4.106.139:/var/www/html/Bidding/
scp -r ./BidInfo/ root@121.4.106.139:/var/www/html/Bidding/
scp -r ./templates/ root@121.4.106.139:/var/www/html/Bidding/
#echo ''
#allfiles=(`ls`)
#for var1 in ${allfiles[@]};do
 #  echo $var1
#done
