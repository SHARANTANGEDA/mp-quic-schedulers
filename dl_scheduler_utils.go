package quic

import (
	"fmt"
	"log"
	"os"

	"github.com/SHARANTANGEDA/mp-quic/internal/protocol"
)

func (sch *scheduler) logTrainingData(s *session, selectedPath *path, trainingFile string) {

	var secondBestPath *path
	if selectedPath == nil {
		return
	}

	for pathID, pth := range s.paths {
		// XXX Prevent using initial pathID if multiple paths
		if pathID == protocol.InitialPathID || pathID == selectedPath.pathID {
			continue
		} else {
			secondBestPath = pth
			break
		}
	}
	if secondBestPath == nil {
		return
	}
	//Features
	cwndBest := float64(selectedPath.sentPacketHandler.GetCongestionWindow())
	cwndSecond := float64(secondBestPath.sentPacketHandler.GetCongestionWindow())
	inflightFirst := float64(selectedPath.sentPacketHandler.GetBytesInFlight())
	inflightSecond := float64(secondBestPath.sentPacketHandler.GetBytesInFlight())
	bestPathRTT := selectedPath.rttStats.LatestRTT()
	secondBestPathRTT := secondBestPath.rttStats.LatestRTT()
	firstPathAvgRTT := selectedPath.rttStats.SmoothedRTT()
	secondPathAvgRTT := secondBestPath.rttStats.SmoothedRTT()
	selectedPathId := selectedPath.pathID

	file, err := os.OpenFile(trainingFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, os.ModePerm)
	if err != nil {
		log.Fatal(err)
	}
	if sch.WriteHeaderColumn {
		file.WriteString("path_id,cwnd_1,cwnd_2,in_flight_1,in_flight_2,rtt_1,rtt_2,avg_rtt_1,avg_rtt_2")
		file.WriteString(fmt.Sprintf("\n%d,%f,%f,%f,%f,%d,%d,%d,%d", selectedPathId, cwndBest, cwndSecond,
			inflightFirst, inflightSecond, bestPathRTT, secondBestPathRTT, firstPathAvgRTT, secondPathAvgRTT))
		sch.WriteHeaderColumn = false
	} else {
		file.WriteString(fmt.Sprintf("\n%d,%f,%f,%f,%f,%d,%d,%d,%d\n", selectedPathId, cwndBest, cwndSecond,
			inflightFirst, inflightSecond, bestPathRTT, secondBestPathRTT, firstPathAvgRTT, secondPathAvgRTT))
	}
	_ = file.Close()
}
