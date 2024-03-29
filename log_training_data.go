package quic

import (
	"fmt"
	"github.com/SHARANTANGEDA/mp-quic/internal/protocol"
	"os"
)

//
//func (s *server) startTraining() {
//	fmt.Println("Started Training Task Scheduler")
//	trainCmd := fmt.Sprintf("from mpquic_schedulers import neural_net; neural_net.train_update_model('%s', %d, '%s')",
//		s.config.OnlineTrainingFile, s.config.TrainingEpochs, s.config.ModelOutputDir)
//
//	fmt.Println(trainCmd)
//	cmd := exec.Command(s.config.PythonEnv, "-c", trainCmd)
//	//var out bytes.Buffer
//	var stderr bytes.Buffer
//	//cmd.Stdout = &out
//	cmd.Stderr = &stderr
//
//	if err := cmd.Run(); err != nil {
//		fmt.Println("Error in script execution: ", err.Error(), "::", stderr.String())
//	}
//	fmt.Println("Training Started at process Id:", cmd.Process.Pid)
//}

func (sch *scheduler) logTrainingData(s *session, selectedPath *path, trainingFile string) {

	var secondBestPath *path
	if selectedPath == nil || selectedPath.pathID == protocol.InitialPathID {
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

	_, err := os.Stat(trainingFile)
	if err != nil {
		return
	}

	file, err := os.OpenFile(trainingFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, os.ModePerm)
	if err != nil {
		fmt.Println("Error in file: ", err, trainingFile)
	}

	file.WriteString(fmt.Sprintf("\n%d,%f,%f,%f,%f,%d,%d,%d,%d", selectedPathId, cwndBest, cwndSecond,
		inflightFirst, inflightSecond, bestPathRTT, secondBestPathRTT, firstPathAvgRTT, secondPathAvgRTT))
	_ = file.Close()
}
