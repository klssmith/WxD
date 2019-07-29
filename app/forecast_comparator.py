#!/usr/local/bin python3

from datetime import datetime
# now=$(date +"%T")
# echo "hey hey hey it is $now"

with open('results.txt', 'a') as f:
    f.write(f'The time is {datetime.now()}\n')
    f.write('blah\n')

# get the heathrow forecast
# forecast = client.get_3hourly_forecasts_for_site(3772)
