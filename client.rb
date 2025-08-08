require 'net/http'
require 'json'
require 'uri'

class RPCClient
  def initialize(url)
    @uri = URI(url)
    @http = Net::HTTP.new(@uri.host, @uri.port)
    @id = 0
  end

  def call(method, *params)
    @id += 1
    request = {
      jsonrpc: '2.0',
      method: method,
      params: params,
      id: @id
    }

    http_req = Net::HTTP::Post.new(@uri)
    http_req['Content-Type'] = 'application/json'
    http_req.body = request.to_json

    response = JSON.parse(@http.request(http_req).body)

    if response['error']
      raise "RPC Error (#{response['error']['code']}): #{response['error']['message']}"
    end

    response['result']
  end

  def method_missing(method_name, *args)
    call(method_name, *args)
  end
end

client = RPCClient.new('http://localhost:8000')

puts client.add(5, 3)
puts client.echo("hello", 3)

begin
  puts client.divide(10, 0)
rescue => e
  puts e.message
end

puts client.add(100, 23)
