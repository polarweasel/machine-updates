# Machine status tracking

I've got a little 5.5cm 3-colour epaper display. And I've got a Raspberry Pi that's on all the time, since it's a Pi-Hole. And there are a couple of other usually-on machines hanging around, too. So, I figured I should put the display to use and show some status for these machines.

But then the question came up: _How do I get the other machines to tell the Pi-Hole about themselves once in a while_? I could write a shell script that runs some commands over SSH on each machine, but an API sounded like more fun, so here we are.

## Go server

To generate the sample Go server from the API spec:

```bash
java -jar ../swagger-codegen/swagger-codegen-cli.jar generate -i api-specs/machine-status.yaml -l go-server -o go-server
```

And every time you regenerate it, you need to fix the `import` statement in `main.go` to update the `sw` line to read as follows:

```go
  sw "example/go-server/go"
```

## Python client

The client and configuration file are in `/client`. This should be ready to go once the server exists. It does send valid output according to the mocking server, at least!

## Mocking server

This is why Redocly is included in this repo...

```bash
# Pick up the current changes to the API spec
npm run bundle-internal

# Run the mocking server
npm run mock-internal
```
