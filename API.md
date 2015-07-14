#API request

##Authentication requests

####Request a user for auth
* **Path:** `api/applications/auth/request/`
* Parameters
  * `username` username
  * `client_id` client_id of the application
* Responses
  * `400` if parameter is missing
  * `404` if username or client_id was not found
  * `200` if reuqest succeeded with json data `{'n':<UTC timestamp>}`

####Request to auth a user
* **Path:** `api/applications/auth/user/`
* Parameters
  * `username` username
  * `password` password
  * `client_id` client_id of the application
  * `n` timestamp from auth request
  * `token` hash of n and application secret
* Responses
  * `400` if parameter is missing
  * `403` if username, password or token is wrong
  * `404` if client_id or n is not found
  * `200` if reuqest succeeded with json data `{'n':<64Bit Ineger>, 'u':<int>, 'token':<Hash token>}`

####Request to revoke a user auth
* **Path:** `api/applications/auth/revoke/`
* Parameters
  * `u` int
  * `token` hash of n and token
* Responses
  * `400` if parameter is missing
  * `403` if token is wrong
  * `404` if username was not found
  * `200` if reuqest succeeded

##General requests

###Get the leaderboard
* **Path:** `/api/leaderboard/`
* Responses
  * `200` if reuqest succeeded with json data `{'response_date':<UTC timestamp>, 'leaderboard':[{'citizen_scientist':<Username>, 'points':<Points>, 'languages': [{'language':<Code>}], 'cultural_background':<Cultural background>}]}`

###Get the statistics
* **Path:** `/api/statistics/`
* Responses
  * `200` if reuqest succeeded with json data `{'response_date':<UTC timestamp>, 'statistics': [{'citizen_scientists':<Number of citizen scientists>, 'languages':[{'language':<Code>, 'words':<Number of words>, 'associations':<Number of associations>}]}]}`

###Get the association history of a user
* **Path:** `/api/profile/associationhistory/`
* Parameters
  * `u` username
  * `token` hash of n and token
* Responses
  * `400` if parameter is missing
  * `403` if token is wrong
  * `404` if username was not found
  * `200` if reuqest succeeded with json data `{'response_date':<UTC timestamp>}`

##Association request

###Get a list of all available languages
* **Path:** `/api/languages/`
* Responses
  * `200` if reuqest succeeded with json data `{'response_date':<UTC timestamp>, 'languages': [{'name':<Name>, 'code':<Code>}]}`

###Get the next word to associate
* **Path:** `/api/words/next/`
* Parameters
  * `language` language of the word
  * `username` username of a user (optinal)
  * `excludes` list of words that should be exclude from the result (optinal)
* Responses
  * `400` if parameter is missing
  * `404` if language or username was not found
  * `200` if reuqest succeeded with json data `{'word':<Word>}`

###Check if a word is a word
* **Path:** `/api/words/isa/`
* Parameters
  * `language` language of the word
  * `word` word to check
* Responses
  * `400` if parameter is missing
  * `404` if language or word was not found
  * `200` if reuqest succeeded

##Export words with their associations
* **Path:** `/api/words/`
* Parameters
  * `language` language of the word (optional)
  * `word` list of word ids to include (optional)
  * `limit` limit the number of associations per word
* Responses
  * `200` if reuqest succeeded with json data `{'response_date':<UTC timestamp>, 'words':[{'word':<Word>, 'language':<Code>, 'identifier':<OAI-PMH identifier>, 'url':<Website URL>, 'associations': [{'word':<Word>, 'language':<Code>, 'identifier':<OAI-PMH identifier>, 'url':<Website URL>, 'json_url':<JSON export URL>, 'count':<Count of the associations>}]}]}`

##OAI-PMH
* **Path:** `/oai2/`
* [http://www.openarchives.org/pmh/](http://www.openarchives.org/pmh/)
