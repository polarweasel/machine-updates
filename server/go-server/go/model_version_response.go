/*
 * Machine status API
 *
 * Helps to track status of networked machines.
 *
 * Contact: awball@polarweasel.org
 */
package swagger

type VersionResponse struct {
	// The API version
	Version string `json:"version"`
}
