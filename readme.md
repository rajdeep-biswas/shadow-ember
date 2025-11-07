# Data Dump

Running `curl https://epic.gsfc.nasa.gov/api/natural -o dump.json` gives me a JSON file but it says `"date":"2025-07-15 04:53:34"` (today is 7th Nov), so I need to look for an API that gives me *today's* data.

"Due to the lapse in federal government funding, NASA is not updating this website. We sincerely regret this inconvenience.", says the webpage header. Fuck the US Government lmao.

I'll just fetch today minus 5 years and pretend that it's the "latest" data every day.

And oh, it's as simple as doing -  
`curl https://epic.gsfc.nasa.gov/api/enhanced/date/<yyyy-mm-dd>  -o <filename>.json`

