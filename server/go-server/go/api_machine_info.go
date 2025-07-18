/*
 * Machine status API
 *
 * Helps to track status of networked machines.
 *
 * Contact: awball@polarweasel.org
 */
package swagger

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
)

// GET /machine-status/machines
func GetAllMachines(w http.ResponseWriter, r *http.Request) {
	// Populate the machine list
	machineList, err := getMachineList()
	if err != nil {
		log.Print(err.Error())
		http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		return
	}

	// Output the machine list as jSON
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(machineList)
}

// GET /machine-status/machines/{machineId}
func GetMachine(w http.ResponseWriter, r *http.Request) {
	// Get the machine ID from the path variable
	vars := mux.Vars(r)
	machineId := vars["machineId"]

	// Populate the machine object
	machine, err := getMachine(machineId)
	if err != nil {
		log.Print(err.Error())
		http.Error(w, http.StatusText(http.StatusNotFound), http.StatusNotFound)
		return
	}

	// Output the machine object as JSON
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(machine)
}

// PUT /machine-status/machines/{machineId}
func UpdateMachine(w http.ResponseWriter, r *http.Request) {
	// Much of the code in this function is from
	// https://www.alexedwards.net/blog/how-to-properly-parse-a-json-request-body

	// If the Content-Type header is present, check that it's `application/json`.
	//
	// Then, parse and normalize the header, removing any additional
	// parameters (like charset or boundary information) and normalizing it
	// by stripping whitespace and converting to lowercase before checking
	// the value.
	ct := r.Header.Get("Content-Type")
	if ct != "" {
		mediaType := strings.ToLower(strings.TrimSpace(strings.Split(ct, ";")[0]))
		if mediaType != "application/json" {
			msg := "Content-Type header must be application/json"
			http.Error(w, msg, http.StatusUnsupportedMediaType)
			return
		}
	}

	// Limit request bodies to 1500 bytes. Anything larger results in
	// Decode() returning a "http: request body too large" error.
	r.Body = http.MaxBytesReader(w, r.Body, 1500)

	// Set up the JSON decoder and prohibit unknown (non-ignored) fields.
	dec := json.NewDecoder(r.Body)
	dec.DisallowUnknownFields()

	var machine Machine

	// Decode the request body into the Machine object
	err := dec.Decode(&machine)
	if err != nil {
		var syntaxError *json.SyntaxError
		var unmarshalTypeError *json.UnmarshalTypeError
		var maxBytesError *http.MaxBytesError

		switch {
		// Catch JSON syntax errors, and send an error message
		// which interpolates the location of the problem to make it
		// easier for the client to fix.
		case errors.As(err, &syntaxError):
			msg := fmt.Sprintf("Request body contains badly-formed JSON (at position %d)", syntaxError.Offset)
			http.Error(w, msg, http.StatusBadRequest)

		// In some circumstances, Decode() may return an
		// io.ErrUnexpectedEOF error for JSON syntax errors. See
		// https://github.com/golang/go/issues/25956.
		case errors.Is(err, io.ErrUnexpectedEOF):
			msg := "Request body contains badly-formed JSON"
			http.Error(w, msg, http.StatusBadRequest)

		// Catch type errors, like trying to assign a string in the
		// JSON request body to an int field in the Machine struct. Again,
		// interpolate the relevant field name and position into the error.
		case errors.As(err, &unmarshalTypeError):
			msg := fmt.Sprintf("Request body contains an invalid value for the %q field (at position %d)", unmarshalTypeError.Field, unmarshalTypeError.Offset)
			http.Error(w, msg, http.StatusBadRequest)

		// There are unexpected fields in the request body.
		// Interpolate the field name in the error message.
		// There is an open issue at
		// https://github.com/golang/go/issues/29035 regarding
		// turning this into a sentinel error.
		case strings.HasPrefix(err.Error(), "json: unknown field "):
			fieldName := strings.TrimPrefix(err.Error(), "json: unknown field ")
			msg := fmt.Sprintf("Request body contains unknown field %s", fieldName)
			http.Error(w, msg, http.StatusBadRequest)

		// Decode() returns an io.EOF error if the request body is empty.
		case errors.Is(err, io.EOF):
			msg := "Request body must not be empty"
			http.Error(w, msg, http.StatusBadRequest)

		// Request body is too large.
		case errors.As(err, &maxBytesError):
			msg := fmt.Sprintf("Request body must not be larger than %d bytes", maxBytesError.Limit)
			http.Error(w, msg, http.StatusRequestEntityTooLarge)

		// Default: log the error and send a 500 Internal Server Error response.
		default:
			log.Print(err.Error())
			http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		}
		return
	}

	// Check for more JSON objects in the request body.
	// Call Decode again, using a pointer to an empty anonymous struct as
	// the destination. If the request body only contained a single JSON
	// object this will return an io.EOF error. So if we get anything else,
	// we know that there is additional data in the request body.
	err = dec.Decode(&struct{}{})
	if !errors.Is(err, io.EOF) {
		msg := "Request body must only contain a single JSON object"
		http.Error(w, msg, http.StatusBadRequest)
		return
	}

	// Persist the machine data
	if err := updateMachine(machine); err != nil {
		log.Print(err.Error())
		http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		return
	}

	// Send HTTP 201 "created" response
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusCreated)
}

// DELETE /machine-status/machines/{machineId}
func DeleteMachine(w http.ResponseWriter, r *http.Request) {
	// Get the machine ID from the path variable
	vars := mux.Vars(r)
	machineId := vars["machineId"]

	// Delete the machine data
	if err := deleteMachine(machineId); err != nil {
		log.Print(err.Error())
		http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		return
	}

	// Send HTTP 204 "no content" response
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusNoContent)
}

// GET /machine-status/vibes
func VibeCheck(w http.ResponseWriter, r *http.Request) {
	// The vibe check should be good if nothing has any flags
	// - open the store
	// - search

	var overall_vibe vibeResponse

	overall_vibe, err := getVibes()
	if err != nil {
		fmt.Print("How'd we break the vibes?")
	}
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(overall_vibe)
	//fmt.Fprintf(w, "No vibes yet, but API version is %s\n", APIVersion)
}
