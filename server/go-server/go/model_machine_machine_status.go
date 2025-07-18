/*
 * Machine status API
 *
 * Helps to track status of networked machines.
 *
 * Contact: awball@polarweasel.org
 */
package swagger

type MachineMachineStatus struct {
	LoadAverages *LoadAverages `json:"loadAverages"`

	DiskFree *DiskFree `json:"diskFree"`
}
