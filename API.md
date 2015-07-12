#API request

##Get a list of all available languages
* **Path:** `/api/languages/`

##Get the leaderboard
* **Path:** `/api/leaderboard/`

##Get the statistics
* **Path:** `/api/statistics/`

##Export words with their associations
* **Path:** `/api/words/`
* Parameters
  * `language` language of the word (optional)
  * `word` list of word ids to include (optional)
  * `limit` limit the number of associations per word

##Get the next word to associate
* **Path:** `/api/words/next/`
* Parameters
  * `language` language of the word
  * `username` username of a user (optinal)
  * `excludes` list of words that should be exclude from the result (optinal)

##Check if a word is a word
* **Path:** `/api/words/isa/`
* Parameters
  * `language` language of the word
  * `word` word to check

##OAI-PMH
[http://www.openarchives.org/pmh/](http://www.openarchives.org/pmh/)
* **Path:** `/oai2/`
