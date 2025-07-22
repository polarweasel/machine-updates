/*
 * A single machine
 */
package swagger

import "time"

type Machine struct {
	Name string `json:"name"`
	// Optional description of the machine (not useful in a small UI)
	MachineDescription string `json:"machineDescription,omitempty"`

	// Timestamping on the server side avoids any issues with the
	// client machine's time being off.
	Timestamp time.Time `json:"updateTimestamp,omitempty"`

	MachineStatus *MachineMachineStatus `json:"machineStatus"`
}
