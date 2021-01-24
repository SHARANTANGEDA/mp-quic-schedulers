# A Standalone MPQUIC implementation in pure Go

**Inspired and based on: https://multipath-quic.org/2017/12/09/artifacts-available.html**

mp-quic is a multipath implementation of the [quic-go](https://github.com/lucas-clemente/quic-go) protocol

## Roadmap
- Implement different Machine Learning based Schedulers
- _DONE_: Make this completely standalone, so that anyone can import this library without manual

This version of mp-quic is not dependent on quic-go, and can be installed as a standalone package

### Pre-Requisites

- Install hdf5 library in your PC before executing this 
	
	In mac: ` brew install hdf5`
	
	In Ubuntu: 	`  sudo apt-get install libhdf5-serial-dev`


- Run ` export GOPRIVATE=github.com/SHARANTANGEDA` in command-line before importing private-packages

- Then `go get -t -u ./...`

## Guides

We currently support Go **_1.14+_**

Essential Environment Variables: `OUTPUT_DIR="ABSOLUTE_PATH_TO_OUTPUT_DIR` is needed for 
scheduler implementation in native application

Choosing Schedulers:

    // Available Schedulers: round_robin, low_latency
    // Default Scheduler: round_robin
    // To choose a custom scheduler you can follow the below approach:
    cfgServer := &quic.Config{
		CreatePaths: true,
		Scheduler: 'round_robin', // Or any of the above mentioned scheduler
		WeightsFile: '/file/path'
		Training: true,
		Epsilon: 0.0001
		AllowedCongestion: 50
		DumpExperiences: true
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
