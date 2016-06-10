# Usage

Right now, you can just run:

`run <hz> <seconds>`

where hz is the downsample rate, and seconds is window size in seconds. 

Hopefully, I've written this in a way such that these programs can fail halfway through and be elegantly restarted, as well as run concurrently. We'll see.