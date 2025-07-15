/*
 * Machine status API
 *
 * Helps to track status of networked machines.
 *
 * Contact: awball@polarweasel.org
 */
package swagger

type DiskFreeFreeSpace struct {
	// Available disk space, as an integer percentage
	FreeSpacePercentage int32 `json:"freeSpacePercentage"`
	// True if this should be highlighted, false otherwise
	ProblemFlag bool `json:"problemFlag"`
}
