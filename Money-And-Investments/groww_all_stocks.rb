require "net/http"
require "json"
require "uri"

URL = "https://groww.in/v1/api/stocks_data/v1/all_stocks"

HEADERS = {
  "Content-Type" => "application/json",
  "Accept" => "application/json",
  "User-Agent" => "Mozilla/5.0"
}

all_records = []
page = 0
size = 15

loop do
  payload = {
    listFilters: {
      INDUSTRY: [],
      INDEX: []
    },
    objFilters: {
      CLOSE_PRICE: { min: 0, max: 500_000 },
      MARKET_CAP: { min: 0, max: 3_000_000_000_000_000 }
    },
    page: page.to_s,
    size: size.to_s,
    sortBy: "NA",
    sortType: "ASC"
  }

  uri = URI(URL)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true

  request = Net::HTTP::Post.new(uri.request_uri, HEADERS)
  request.body = payload.to_json

  response = http.request(request)
  json = JSON.parse(response.body)

  records = json["records"] || []

  break if records.empty?

  all_records.concat(records)

  puts "Page #{page} fetched (#{records.size}), total: #{all_records.size}"

  page += 1

  sleep 0.2   # polite rate-limiting (important)
end

puts "Finished. Total records fetched: #{all_records.size}"
