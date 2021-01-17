# A Standalone MPQUIC implementation in pure Go

**Inspired and based on: https://multipath-quic.org/2017/12/09/artifacts-available.html**

mp-quic is a multipath implementation of the [quic-go](https://github.com/lucas-clemente/quic-go) protocol

## Roadmap
- Implement different Machine Learning based Schedulers
- _DONE_: Make this completely standalone, so that anyone can import this library without manual

This version of mp-quic is not dependent on quic-go, and can be installed as a standalone package
## Guides

We currently support Go **_1.12+_**

Choosing Schedulers:

    // Available Schedulers: round_robin, low_latency
    // Default Scheduler: round_robin
    // To choose a custom scheduler you can follow the below approach:
    cfgServer := &quic.Config{
		CreatePaths: true,
		Scheduler: 'round_robin', // Or any of the above mentioned scheduler
	}  // If nothing is mentioned round_robin will be default

Installing and updating dependencies:

    go get -t -u ./...

Running tests:

    go test ./...

## Example Implementation

An application that does File Transfer using mp-quic has been shown at [MPQUIC-FTP](https://github.com/SHARANTANGEDA/mpquic_ftp)

In case of any issue accessing it, please reach out to repository owner

## Contributing

We are always happy to welcome new contributors! We have a number of self-contained issues that are suitable for first-time contributors, they are tagged with [want-help](https://github.com/SHARANTANGEDA/mp-quic/issues?q=is%3Aopen+is%3Aissue+label%3Awant-help). If you have any questions, please feel free to reach out by opening an issue or leaving a comment.

## Acknowledgment
- Thanks to [Qdeconinck](https://github.com/qdeconinck/mp-quic) for starting this amazing work

### Running the example server

    go run example/main.go -www /var/www/

Using the `quic_client` from chromium:

    quic_client --host=127.0.0.1 --port=6121 --v=1 https://quic.clemente.io

Using Chrome:

    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --user-data-dir=/tmp/chrome --no-proxy-server --enable-quic --origin-to-force-quic-on=quic.clemente.io:443 --host-resolver-rules='MAP quic.clemente.io:443 127.0.0.1:6121' https://quic.clemente.io

### QUIC without HTTP/2

Take a look at [this echo example](example/echo/echo.go).

### Using the example client

    go run example/client/main.go https://clemente.io

## Usage

### As a server

See the [example server](example/main.go) or try out [Caddy](https://github.com/mholt/caddy) (from version 0.9, [instructions here](https://github.com/mholt/caddy/wiki/QUIC)). Starting a QUIC server is very similar to the standard lib http in go:

```go
http.Handle("/", http.FileServer(http.Dir(wwwDir)))
h2quic.ListenAndServeQUIC("localhost:4242", "/path/to/cert/chain.pem", "/path/to/privkey.pem", nil)
```

### As a client

See the [example client](example/client/main.go). Use a `h2quic.RoundTripper` as a `Transport` in a `http.Client`.

```go
http.Client{
  Transport: &h2quic.RoundTripper{},
}
```
