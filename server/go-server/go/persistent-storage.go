/*
* Utility functions for persistent storage.
* This is using BitCask: https://git.mills.io/prologic/bitcask
 */
package swagger

import (
	"log"

	"go.mills.io/bitcask/v2"
)

func deleteMachine(machineId string) error {
	db, err := bitcask.Open("test.db")
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer db.Close()

	c := db.Collection("machines")

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
	db, err := bitcask.Open("test.db")
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer db.Close()

	c := db.Collection("machines")

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
	db, err := bitcask.Open("test.db")
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer db.Close()

	c := db.Collection("machines")

	var machineList []Machine

	if err := c.List(&machineList); err != nil {
		log.Printf("Machine list is empty")
		return machineList, err
	}

	return machineList, nil
}

func updateMachine(machineData Machine) error {
	db, err := bitcask.Open("test.db")
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer db.Close()

	c := db.Collection("machines")

	if err := c.Add(machineData.Name, machineData); err != nil {
		log.Printf("error adding %s to database: %v", machineData.Name, err)
		return err
	}

	return nil
}
