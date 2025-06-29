# Machine status tracking

I've got a little 5.5cm 3-colour epaper display. And I've got a Raspberry Pi that's on all the time, since it's a Pi-Hole. And there are a couple of other usually-on machines hanging around, too. So, I figured I should put the display to use and show some status for these machines.

But then the question came up: _How do I get the other machines to tell the Pi-Hole about themselves once in a while_? I could write a shell script that runs some commands over SSH on each machine, but an API sounded like more fun, so here we are.

And here is a runon sentence with one, two and three items.
