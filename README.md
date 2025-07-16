# Machine status tracking

I've got a little 5.5cm 3-colour epaper display. And I've got a Raspberry Pi that's on all the time, since it's a Pi-Hole. And there are a couple of other usually-on machines hanging around, too. So, I figured I should put the display to use and show some status for these machines.

But then the question came up: _How do I get the other machines to tell the Pi-Hole about themselves once in a while_? I could write a shell script that runs some commands over SSH on each machine, but an API sounded like more fun, so here we are.

## Installation

To get this running for yourself, you'll need a machine to run the server, and one or more machines to run the client.

**To install the server** (I'm assuming Debian/Ubuntu here, but I imagine this will work on most distros that use systemd):

1. On the server machine, clone or copy this repo.
1. Compile the binary with `go build`.
1. As root, move the `machine-status` executable to `/usr/local/bin/`, renaming as required.
1. As root, copy the [system service file](config-files/machine-status.service) to `/etc/systemd/system/`.
1. Run a few commands to get things started:

  ```sh
  sudo systemctl daemon-reload
  sudo systemctl enable machine-status.service
  sudo systemctl start machine-status.service
  ```

1. Verify that the service is running:

  ```sh
  sudo systemctl status machine-status.service
  ```

**To install the client** (I'm assuming you have a recent python3 installed):

1. On the client machine, copy [machine-status-update.py](client/machine-status-update.py) to /usr/local/bin and make it executable:

  ```sh
  sudo cp client/machine-status-update.py /usr/local/bin/machine-status-update
  sudo chmod +x /usr/local/bin/machine-status-update
  ```

1. Make a directory to hold [config.toml](config-files/config.toml), and copy the file into it:

  ```sh
  sudo mkdir /etc/machine-status-update
  sudo cp config-files/config.toml /etc/machine-status-update
  ```

1. Adjust the settings in `config.toml` as required. At a minimum, you'll want to change `machine_status_ip` to the IP address or hostname of the machine running the server.

1. Copy the [machine-status-cron](config-files/machine-status-cron) file to the system's cron-job directory:

  ```sh
  sudo cp config-files/machine-status-cron /etc/cron.d/machine-status-cron
  ```

1. Run the client, and fix any Python dependency issues that come up...

  ```sh
  /usr/local/bin/machine-status-update
  ```

Finally, wait a bit (is your cron job running at the default 5-minute interval, or did you make it longer?), then query the server to see if everything is working...

```sh
curl http://servername:8080/machine-status/machines
```

(You should get a JSON object back, showing the status of any configured client machines.)

## Go server

To generate the sample Go server from the API spec:

```bash
java -jar ../swagger-codegen/swagger-codegen-cli.jar generate -i api-specs/machine-status.yaml -l go-server -o go-server
```

And every time you regenerate it, you need to fix the `import` statement in `main.go` to update the `sw` line to read as follows:

```go
  sw "polarweasel/machine-status/go"
```

(This is a reference to the `module` entry on line 1 of [go.mod](server/go-server/go.mod). If you use this code, change both to suit your situation.)

### Generate Go models only

Or... just generate the models, and leave the implementation code alone. (This is using the [selective generation](https://github.com/swagger-api/swagger-codegen/blob/3.0.0/docs/generation-selective.md) options.)

```bash
# Run this from the `server` directory
java -Dmodels -DmodelDocs=false -DmodelTests=false \
     -jar ../swagger-codegen/swagger-codegen-cli.jar \
     generate -i api-specs/machine-status.yaml \
     -l go-server \
     -o go-server
```

## Python client

The client and configuration file are in `/client`. This should be ready to go once the server exists. It does send valid output according to the mocking server, at least!

## Mocking server

This is why Redocly is included in this repo...

Note that the API is slightly out of sync with the implementation, because I wimped out on implementing the `problem+json` error format.

```bash
# Pick up the current changes to the API spec
npm run bundle-internal

# Run the mocking server
npm run mock-internal
```
