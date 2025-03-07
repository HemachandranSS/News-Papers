#dynamic value
dd_mm_yyyy = "31032014"
end_page = 100
file_format = "pdf"

Dir.mkdir(dd_mm_yyyy) unless Dir.exist?(dd_mm_yyyy)

base_url_path = "https://emagazine-static.tosshub.com/emag/production/epaperimages"
file_url = "#{base_url_path}/#{dd_mm_yyyy}/#{dd_mm_yyyy}-md-hr"

#iteration
Dir.chdir(dd_mm_yyyy) do
  (1..end_page).each do |val|
    begin
      command = "wget #{file_url}-#{val}.#{file_format}"
      system(command)
    rescue => e
      puts "No File Found"
      next
    end
  end
end
