#API request

##Authentication requests
Each request that requires a user to be authenticated check first if the provided
u and token are correct. If during an error occurs during this one of the
following responses will be send:
* **400**: Required parameter "u" or "token" is missing.
* **403**: Wrong "token" given.
* **404**: AuthedUser with "u" not found.

The u is the int value received in the response of a successful authentication.
The token is a sha512 of the token and n received in the response of a successful
authentication. For each request the n that will be hashed needs to be n+1 unless
the request fails with one of the three above listed errors. In any other
response even if it is an error response need to generate a new token with n+1
if a new request.

####Request a user for auth
* **Path:** `/api/applications/auth/request/`
* Parameters
  * `username` username
  * `client_id` client_id of the application
* Responses
  * `400` if parameter is missing
  * `404` if username or client_id was not found
  * `200` if reuqest succeeded with json data `{'timestamp':<UTC timestamp>}`

####Request to auth a user
* **Path:** `/api/applications/auth/user/`
* Parameters
  * `username` username
  * `password` password
  * `client_id` client_id of the application
  * `timestamp` timestamp from auth request
  * `token` hash of application secret and timestamp
* Responses
  * `400` if parameter is missing
  * `403` if username, password or token is wrong
  * `404` if client_id or n is not found
  * `200` if reuqest succeeded with json data `{'n':<unit>, 'u':<int>, 'token':<Hash token>}`

####Request to revoke a user auth
* **Path:** `/api/applications/auth/revoke/`
* Parameters
  * `u` int
  * `token` hash of user token and n
* Responses
  * `400` if parameter is missing
  * `403` if token is wrong
  * `404` if u was not found
  * `200` if reuqest succeeded ```{"response_date":<UTC timestamp>}```

##General requests

###Get the leaderboard
* **Path:** `/api/leaderboard/`
* Responses
  * `200` if reuqest succeeded with json data `{'response_date':<UTC timestamp>, 'leaderboard':[{'citizen_scientist':<Username>, 'points':<Points>, 'languages': [{'language':<Code>}], 'cultural_background':<Cultural background>}]}`

###Get the statistics
* **Path:** `/api/statistics/`
* Responses
  * `200` if reuqest succeeded with json data `{'response_date':<UTC timestamp>, 'statistics': [{'citizen_scientists':<Number of citizen scientists>, 'languages':[{'language':<Code>, 'words':<Number of words>, 'associations':<Number of associations>}]}]}`

##Profile requests

###Get the profile of a user
* **Path:** `/api/profile/`
* Parameters
  * `u` int
  * `token` hash of n and token
* Responses
  * `400` if parameter is missing
  * `403` if token is wrong
  * `404` if u was not found
  * `200` if reuqest succeeded with json data
  ```
  {"response_date":<UTC timestamp>,
   "association_history":[{"points":<Points>,
                           "association":{"count":<Count>,
                                          "word":{"word":<Word>,
                                                  "language":<Code>,
                                                  "identifier":<OAI-PMH identifier>,
                                                  "url":<Website URL>,
                                                  "json_url":<JSON export URL>},
                                          "association":{"word":<Word>,
                                                  "language":<Code>,
                                                  "identifier":<OAI-PMH identifier>,
                                                  "url":<Website URL>,
                                                  "json_url":<JSON export URL>}}}
                         ]}
  ```

###Get the association history of a user
* **Path:** `/api/profile/associationhistory/`
* Parameters
  * `u` int
  * `token` hash of n and token
* Responses
  * `400` if parameter is missing
  * `403` if token is wrong
  * `404` if u was not found
  * `200` if reuqest succeeded with json data
  ```
  {"response_date":<UTC timestamp>,
   "profile":{"username":<Username>,
               "points":<Points>,
               "cultural_background":<Cultural background>,
               "first_name":<First name>,
               "last_name":<Last name>,
               "email":<Email address>
  ```

###Adds a word to the list of exclude list of the user
* **Path:** `/api/profile/excludedwords/add/`
* Parameters
  * `u` int
  * `token` hash of n and token
  * `word` word to add to exclude list
  * `language` language of the word
* Responses
  * `400` if parameter is missing
  * `403` if token is wrong
  * `404` if u, word or language was not found
  * `200` if reuqest succeeded with json data
  ```
  {"response_date":<UTC timestamp>,
   "create":<True if a new entry was created else False>}
  ```

###Checks if a word is on the list of excluded words of the user
* **Path:** `/api/profile/excludedwords/exists/`
* Parameters
  * `u` int
  * `token` hash of n and token
  * `word` word to add to exclude list
  * `language` language of the word
* Responses
  * `400` if parameter is missing
  * `403` if token is wrong
  * `404` if u, word or language was not found or if the word is not on the list
  * `200` if reuqest succeeded with json data/word is on the users exclude list
  ```
  {"response_date":<UTC timestamp>}
  ```

###Lists all excluded words of the user
* **Path:** `/api/profile/excludedwords/lists/`
* Parameters
  * `u` int
  * `token` hash of n and token
* Responses
  * `400` if parameter is missing
  * `403` if token is wrong
  * `404` if u was not found
  * `200` if reuqest succeeded with json data
  ```
  {"response_date":<UTC timestamp>,
   "words":[{"word":<Word>,
            "language":<Code>,
            "identifier":<OAI-PMH identifier>,
            "url":<Website URL>,
            "json_url":<JSON export URL>}
  ]}
  ```

##Association request

###Get a list of all available languages
* **Path:** `/api/languages/`
* Responses
  * `200` if reuqest succeeded with json data `{'response_date':<UTC timestamp>, 'languages': [{'name':<Name>, 'code':<Code>}]}`

###Save a association
* **Path:** `/api/association/`
* Parameters
  * `language` language code of the word and association
  * `word` the word
  * `association` the association
  * `u` int
  * `token` hash of n and token
* Responses
  * `400` if parameter is missing
  * `403` if token is wrong
  * `404` if u, language, word was not found
  * `200` if reuqest succeeded with json data
  ```
  {"response_date":<UTC timestamp>, "points":<Points>}
  ```

##Export words with their associations
* **Path:** `/api/words/`
* Parameters
  * `language` language of the word (optional)
  * `word` list of word ids to include (optional)
  * `limit` limit the number of associations per word (optinal)
* Responses
  * `200` if reuqest succeeded with json data
 ```
 {"response_date":<UTC timestamp>,
  "words":[{"word":<Word>,
            "language":<Code>,
            "identifier":<OAI-PMH identifier>,
            "url":<Website URL>,
            "json_url":<JSON export URL>,
            "associations': [{"word":<Word>,
                              "language":<Code>,
                              "identifier":<OAI-PMH identifier>,
                              "url':<Website URL>,
                              "json_url":<JSON export URL>,
                              "count":<Count of the associations>}
            ]}
  ]}
 ```

###Graph data for d3 word graph
* **Path:** `/api/words/graph/`
* Parameters
  * `language` language of the word
  * `word` word
  * `depth` depth of the associations (default 2)
* Responses
  * `400` if parameter is missing
  * `404` if word not found
  * `200` if reuqest succeeded with json data
 ```
 {"nodes":[{"group":<Group>,
            "name":<Word>,
            "id":<ID>}
  ],
  "links":[{"value":<Count of association>,
            "target":<Target node ID>,
            "source":<Source node ID>}
  ],
  "response_date":<UTC timestamp>}
 ```

###Check if a word is a word
* **Path:** `/api/words/isa/`
* Parameters
  * `language` language of the word
  * `word` word to check
* Responses
  * `400` if parameter is missing
  * `404` if language or word was not found
  * `200` if reuqest succeeded ```{"response_date":<UTC timestamp>}```

###Get the next word to associate
* **Path:** `/api/words/next/`
* Parameters
  * `language` language of the word
  * `username` username of a user (optinal)
  * `excludes` list of words that should be exclude from the result (optinal)
* Responses
  * `400` if parameter is missing
  * `404` if language or username was not found
  * `200` if reuqest succeeded with json data `{"response_date":<UTC timestamp>, "word":<Word>}`

##OAI-PMH
* **Path:** `/oai2/`
* [http://www.openarchives.org/pmh/](http://www.openarchives.org/pmh/)
