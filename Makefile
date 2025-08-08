server:
	python3 server.py

client:
	ruby client.rb

all: server client

test:
	curl -X POST http://localhost:8000 \
		-H "Content-Type: application/json" \
		-d '{"jsonrpc":"2.0","method":"add","params":[5,3],"id":1}'
