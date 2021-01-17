package util

func StringInSlice(stringList []string, contains string) bool {
	for _, a := range stringList {
		if a == contains {
			return true
		}
	}
	return false
}
