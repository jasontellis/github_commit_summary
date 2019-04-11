Github Repository Daywise Commit Summary
===
This program prints the average commits 
in given repository for each day of the 
week over the past given no. of weeks
## Dependencies
`Python3`
## To install dependencies:
`pip install -r requirements.txt`

## Instructions for running the program
1. For viewing program help and arguments:<br>
`python main.py -h`

## Tests
1. For running tests: <br>
`python -m unittest test.py git_commit_summary`

## Assumptions
1. Running the program repeatedly will cause the API to fail with a HTTP 403 error once the rate limit of 60 calls 
is exceeded. This can be managed in a production system by checking response header for remaining
 calls and setting timeouts and/or making authenticated calls.
2. This program cannot get commits for more than the past 52 weeks.

Authors
==
[Jason Tellis](https://www.linkedin.com/in/jasontellis91)
