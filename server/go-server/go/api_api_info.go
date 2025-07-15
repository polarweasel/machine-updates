/*
 * API version
 */
package swagger

import (
	"encoding/json"
	"net/http"
)

const APIVersion string = "0.1"

type apiVersion struct {
	ApiVersion string `json:"apiVersion"`
}

func APIVersionList(w http.ResponseWriter, r *http.Request) {
	versionMessage := apiVersion{APIVersion}
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(versionMessage)
}
