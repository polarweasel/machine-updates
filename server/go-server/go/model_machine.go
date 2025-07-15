/*
 * A single machine
 */
package swagger

type Machine struct {
	Name string `json:"name"`
	// Optional description of the machine (not useful in a small UI)
	MachineDescription string `json:"machineDescription,omitempty"`

	MachineStatus *MachineMachineStatus `json:"machineStatus"`
}
