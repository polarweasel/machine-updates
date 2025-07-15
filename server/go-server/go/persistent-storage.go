/*
* Utility functions for persistent storage.
* This is using BitCask: https://git.mills.io/prologic/bitcask
 */
package swagger

import (
	"log"

	"go.mills.io/bitcask/v2"
)

const dbname = "/etc/machine-status/status.db"
const collection = "machines"

func getVibes() (vibeResponse, error) {
	// But actually, we need to iterate through each machine and find out if there's a flag raised.
	db, err := bitcask.Open(dbname)
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer db.Close()

	c := db.Collection(collection)

	var machines []Machine
	c.List(&machines)

	for i := range machines {
		if machines[i].MachineStatus.LoadAverages.ProblemFlag {
			return vibeResponse{false}, nil
		}

		if machines[i].MachineStatus.DiskFree.FreeSpace.ProblemFlag {
			return vibeResponse{false}, nil
		}
	}

	return vibeResponse{true}, nil
}

func deleteMachine(machineId string) error {
	// TODO: put the DB logic in ONE place only (but that might mess with the `defer`)
	db, err := bitcask.Open(dbname)
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer db.Close()

	c := db.Collection(collection)

	// We shouldn't ever hit this path, so definitely crash the app if we do
	if machineId == "" {
		log.Fatalf("Verify this is actually an empty machine ID: %v", machineId)
	}

	if err := c.Delete(machineId); err != nil {
		return err
	}

	return nil
}

func getMachine(machineId string) (Machine, error) {
	db, err := bitcask.Open(dbname)
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer db.Close()

	c := db.Collection(collection)

	// We shouldn't ever hit this path, so definitely crash the app if we do
	if machineId == "" {
		log.Fatalf("Verify this is actually an empty machine ID: %v", machineId)
	}

	var machine Machine

	if err := c.Get(machineId, &machine); err != nil {
		log.Printf("No machine called %s", machineId)
		return machine, err
	}

	return machine, nil
}

func getMachineList() ([]Machine, error) {
	db, err := bitcask.Open(dbname)
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer db.Close()

	c := db.Collection(collection)

	var machineList []Machine

	if err := c.List(&machineList); err != nil {
		log.Printf("Machine list is empty")
		return machineList, err
	}

	return machineList, nil
}

func updateMachine(machineData Machine) error {
	db, err := bitcask.Open(dbname)
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer db.Close()

	c := db.Collection(collection)

	if err := c.Add(machineData.Name, machineData); err != nil {
		log.Printf("error adding %s to database: %v", machineData.Name, err)
		return err
	}

	return nil
}
