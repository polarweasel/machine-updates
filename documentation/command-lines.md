# Command lines

Here are some useful commands you can cut and paste.

* [Redocly commands](#redocly-commands)
* [Spectral and Prism commands](#spectral-and-prism-commands)
* [JSON and YAML processing commands](#command-lines)

**If you don't know about `yq` and `jq`**, skip straight to those [JSON and YAML commands](#other-commands)!

## Redocly commands

View generated docs:

```sh
redocly preview-docs internal@latest
```

Run a live-reload mocking server, including anything marked `x-internal`:

```sh
npm run mock-internal
```

Bundle the spec without anything marked `x-internal`:

```sh
redocly bundle external@latest \
        --output dist/external.yaml
```

Bundle the spec, including stuff marked `internal`:

```sh
redocly split api-specs/machine-status.yaml \
        --outDir temp/internal-split/
```

## Spectral and Prism commands

Lint a spec:

```sh
spectral lint temp/internal-split/openapi.yaml
```

**Prism:** Run a live-reload mocking server:

```sh
prism mock api-specs/machine-status.yaml
```

**Not applicable to machine-status API** Provide the auth headers with your request:

```sh
curl --header "x-token: token" \
     --header "authorization: Bearer token" \
     http://127.0.0.1:4010/vibe
```

Optionally, save a step negotiation media types and include an `accept` header:

```sh
curl --header "accept: application/json" \
     --header "x-token: token" \
     --header "authorization: Bearer token" \
     http://127.0.0.1:4010/vibe
```

Here's the OpenAPI pet store to show validation of requests and responses:

```sh
prism mock \
      https://raw.githubusercontent.com/stoplightio/prism/refs/heads/master/examples/petstore.oas3.yaml

curl -s -D "/dev/stderr" \
     http://127.0.0.1:4010/no_auth/pets/23 | jq
```

### Other commands

Tell curl to make a PUT request, instead of POST, by using the -T argument to upload from a file:

```sh
curl -T good-machine.json \
     -H "Content-Type: application/json" \
     http://localhost:4010/machines/tiny-mines
```

Use the [jq utility](https://jqlang.github.io/jq/) to pretty-print the JSON response from an API call:

```sh
curl -s --header "accept: application/json" \
     http://127.0.0.1:4010/machines | jq
```

Use the [yq utility](https://mikefarah.gitbook.io/yq) to convert the JSON response from an API call to YAML and pretty-print it:

```sh
curl -s --header "accept: application/json" \
     http://127.0.0.1:4010/machines | yq -p json
```
