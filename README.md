# Usage

Right now, you can just run:

`run <hz> <seconds>`

where hz is the downsample rate, and seconds is window size in seconds. 

Hopefully, I've written this in a way such that these programs can fail halfway through and be elegantly restarted, as well as run concurrently. We'll see.

Suggest if you're running on newcastle and not sure how long this will take, use:

`nohup run <hz> <seconds>`

To avoid terminating if your connection gets broken. It's not super great for monitoring Console messages, but I'm sure there's a way around that.