![ALF](http://serialmindsecn.nohup.it/wp-content/uploads/2018/08/ALF-Serie-tv-3.jpg)

# alf
Dispatch efficiently events to external endpoints in your sync app. 
Alf will listen to a unix socket, your process(es) can send messages over the socket to alf, then it
will send them further to your endpoint without blocking your app waiting for the http request to end.


## install
pip install https://github.com/MattBlack85/alf.git

## usage
run `alf /tmp/alf.sock http://example.com`
