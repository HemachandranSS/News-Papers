require 'roo'
require 'roo-xls'
require 'json'

# Load the .xls file
xls = Roo::Excel.new('Vol4105DataBank.xls')

# Get header from the first row
headers = xls.row(1).map(&:to_s)

# Read the data rows
data = []
(2..xls.last_row).each do |i|
  row = Hash[headers.zip(xls.row(i))]
  data << row
end

data = data.reject {|hash_att|  hash_att['Sector'].nil? }

data = data.map do |hash_attr| 
  company_name = hash_attr['Company Name          '].gsub('          ','')
  bse_symbol = hash_attr['BSE Symbol'].to_i
  nse_symbol = hash_attr['NSE Symbol']
  screener_link = "https://www.screener.in/company/#{bse_symbol}"
  business_line_link = "https://www.thehindubusinessline.com/stocks/#{company_name.downcase.gsub(' ', '-').gsub('.','')}"
  google_link = "https://www.google.com/search?q=#{company_name.gsub(' ','%20')}"
  sector = hash_attr['Sector']
  
  {"Company Name" =>  company_name, "BSE Symbol" => bse_symbol, "NSE Symbol" => nse_symbol, "Screener Link" => screener_link, "Business Line Link" => business_line_link, "Google Link" => google_link, "Sector" => sector}
end


grouped_by_sector = data.group_by { |row| row['Sector'].to_s.strip }
grouped_by_sector = grouped_by_sector.sort_by { |sector, _| sector }.to_h

File.open("25_01_2026_listed_companies_grouped_by_sector.json", "w") do |file|
  file.write(grouped_by_sector.to_json)
end


