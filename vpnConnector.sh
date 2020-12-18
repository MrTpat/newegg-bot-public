#!/bin/bash

# ...

openvpn \
	--config "$1" \
	--auth-user-pass <( printf "%s\n%s\n" "$2" "$3" ) \
	--daemon

			    # ...
