/*
 * Machine status API
 *
 * Helps to track status of networked machines.
 *
 * Contact: awball@polarweasel.org
 */
package swagger

// Free space on a machine's main mount of interest.
type DiskFree struct {
	MountPoint string `json:"mountPoint"`

	FreeSpace *DiskFreeFreeSpace `json:"freeSpace"`
}
