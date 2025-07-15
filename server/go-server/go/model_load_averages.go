/*
 * Machine status API
 *
 * Helps to track status of networked machines.
 *
 * Contact: awball@polarweasel.org
 */
package swagger

// A machine's 1/5/15-minute load averages
type LoadAverages struct {
	Load1 float64 `json:"load-1"`

	Load5 float64 `json:"load-5"`

	Load15 float64 `json:"load-15"`
	// True if this should be highlighted, false otherwise
	ProblemFlag bool `json:"problemFlag"`
}
