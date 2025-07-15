/*
 * Machine status API
 *
 * Helps to track status of networked machines.
 *
 * Contact: awball@polarweasel.org
 */
package swagger

import (
	"net/http"

	"github.com/gorilla/mux"
)

type Route struct {
	Name        string
	Method      string
	Pattern     string
	HandlerFunc http.HandlerFunc
}

type Routes []Route

func NewRouter() *mux.Router {
	router := mux.NewRouter().StrictSlash(true)
	for _, route := range routes {
		var handler http.Handler
		handler = route.HandlerFunc
		handler = Logger(handler, route.Name)

		router.
			Methods(route.Method).
			Path(route.Pattern).
			Name(route.Name).
			Handler(handler)
	}

	return router
}

var routes = Routes{
	// APIVersionList is the root of the base path
	// (This API shouldn't answer on / alone)
	Route{
		"APIVersionList",
		"GET",
		"/machine-status/",
		APIVersionList,
	},

	// Delete a single machine's info
	Route{
		"DeleteMachine",
		"DELETE",
		"/machine-status/machines/{machineId}",
		DeleteMachine,
	},

	// Get info for all machines
	Route{
		"GetAllMachines",
		"GET",
		"/machine-status/machines",
		GetAllMachines,
	},

	// Get info for a single machine
	Route{
		"GetMachine",
		"GET",
		"/machine-status/machines/{machineId}",
		GetMachine,
	},

	// Update a single machine's info
	Route{
		"UpdateMachine",
		"PUT",
		"/machine-status/machines/{machineId}",
		UpdateMachine,
	},

	// Get the overall vibe
	Route{
		"VibeCheck",
		"GET",
		"/machine-status/vibe",
		VibeCheck,
	},
}
