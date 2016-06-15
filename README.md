# Usage

Package assumes Anaconda stack has been installed. Usually, this is a large but easy install in a Unix environment. Anaconda is just a manager for a lot of fun python packages like NumPy and SciPy. I've installed a distribution on the SPIN server, and I *think* everyone can use it if they modify their path variable correctly...but I don't know. Come talk to Paul to confirm.

Right now, you can just run:

`./run <hz> <wms> <sms> <oms> <dir>`

where:

hz = target downsample frequency in hz
wms = window size in milliseconds (window over which to calculate features)
sms = skip size in milliseconds (gap between windows)
oms = offset size in milliseconds (amount to cut off back and front of data)
dir = data directory

Hopefully, I've written this in a way such that these programs can fail halfway through and be elegantly restarted, as well as run concurrently. We'll see.

Suggest if you're running on newcastle and not sure how long this will take, use:

`nohup ./run <hz> <wms> <sms> <oms> <dir>`

To avoid terminating if your connection gets broken. It's not super great for monitoring Console messages, but I'm sure there's a way around that.

## No clean run examples

Cleaning files takes a very long time and only really needs to be done once. Here's a quick command for passing the files you've already cleaned to the rest of the programs:

`./nocleanrun 54 6000 1000 1000 csv_for_54_2/clean`

and with nohup:

`nohup ./nocleanrun 54 6000 1000 1000 csv_for_54_2/clean`

and with nohup + console monitoring:

`nohup ./nocleanrun 54 6000 1000 1000 csv_for_54_2/clean & tail -f nohup.out`

## Feature calculation only

Same as cleaning, reducing takes time, and only needs to be done once per downsample rate, so you can run:

`./feature 54 6000 1000 1000 reduced_by_54/`

`nohup ./feature 54 6000 1000 1000 reduced_by_54/`

`nohup ./feature 54 6000 1000 1000 reduced_by_54/ & tail -f nohup.out`
