# Usage

Package assumes Anaconda stack has been installed. Usually, this is a large but easy install in a *nix environment. Anaconda is just a manager for a lot of fun python packages like NumPy and SciPy. I've installed a distribution on the SPIN server, and I *think* everyone can use it if they modify their path variable correctly...but I don't know. Come talk to Paul to confirm.

Right now, you can just run:

`run <hz> <milliseconds>`

where hz is the downsample rate, and seconds is window size in milliseconds. 

Hopefully, I've written this in a way such that these programs can fail halfway through and be elegantly restarted, as well as run concurrently. We'll see.

Suggest if you're running on newcastle and not sure how long this will take, use:

`nohup run <hz> <milliseconds>`

To avoid terminating if your connection gets broken. It's not super great for monitoring Console messages, but I'm sure there's a way around that.

## No clean run examples

Cleaning files takes a very long time and only really needs to be done once. Here's a quick command for passing the files you've already cleaned to the rest of the programs:

`./nocleanrun 54 6000 csv_for_54_2/clean`

and with nohup:

`nohup ./nocleanrun 54 6000 csv_for_54_2/clean`

and with nohup + console monitoring:

`nohup ./nocleanrun 54 6000 csv_for_54_2/clean & tail -f nohup.out`