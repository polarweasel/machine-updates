/*
 * Machine status API
 *
 * Helps to track status of networked machines.
 *
 * Contact: awball@polarweasel.org
 */
package swagger

// Error response for all methods.
type ErrorResponse struct {
	// A reference that identifies the problem type.
	Type_ string `json:"type,omitempty"`
	// A short, human-readable summary of the problem type.
	Title string `json:"title"`
	// HTTP status code from the server.
	Status int32 `json:"status"`
	// A human-readable message describing the error.
	Detail string `json:"detail,omitempty"`
	// A URI reference that identifies the specific occurrence of the problem. It may or may not yield further information if dereferenced.
	Instance string `json:"instance,omitempty"`
}
