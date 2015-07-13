#API request

##Authentication requests

###Request a user for auth
* **Path:** `api/applications/auth/request/`
* Parameters
  * `username` username
  * `client_id` client_id of the application

###Request to auth a user
* **Path:** `api/applications/auth/user/`
* Parameters
  * `username` username
  * `password` password
  * `client_id` client_id of the application
  * `n` timestamp from auth request
  * `hash` hash of n and application secret
* Responses
  * `400` if parameter is missing
  * `404` if client_id or n was not found
  * `405` if username and password or hash is wrong
  * `200` if reuqest succeeded with json data
    * `{'n':<64Bit Ineger>, 'token':<Hash token>}`

###Request to revoke a user auth
* **Path:** `api/applications/auth/revoke/`
* Parameters
  * `username` username
  * `hash` hash of n and token
* Responses
  * `400` if parameter is missing
  * `404` if username was not found
  * `405` if hash was wrong
  * `200` if reuqest succeeded

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
