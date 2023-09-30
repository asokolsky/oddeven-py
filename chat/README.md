# Simple Python Chat Server

https://gist.github.com/nate-onesignal/23668cf3bed0f234529f641bdc2d4cde

Broadcast the chat message via HTTP POST:

- When one client sends a message to the server, the message should be
broadcast to all the clients except the sender;
- Server should handle clients connecting and disconnecting at arbitrary
times;
- Server must broadcast messages to clients without client intervention
(it shouldn’t be necessary for a client to send a message in order to
receive a message or vice versa)

Read the chat messages via HTTP GET

## Testing

python3 -m unittest -v *_test.py
