#API request

##Get a list of all available languages
* **Path:** `/api/languages/`

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