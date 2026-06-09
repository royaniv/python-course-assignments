# Prompts

## Prompt 1

Please create the following in the day8 folder and take the files from day 6 folder. Do not change anything in the day 6 folder.

Make sure it has a "business logic" part that is tested.

Write a web application for it. You can use Flask but it would be nicer if you used one of the other web frameworks of Python.

Make sure they use the same "business logic" functions.

Write some tests for the web application as well.

Include your prompts as well.

## Prompt 2

Use the day 6 PubChem amphiphile script as the starting point, but refactor the day 8 copy so the PubChem lookup and data extraction live in importable business logic functions. Then make both the plotting script and the web application call those same functions.

## Prompt 3

Add pytest tests that avoid real PubChem network calls by using fake response objects. Test the business logic directly and test the web API with an injected fake lookup function.

## Prompt 4

This seems way too elaborate for the stage of the course I am at. Can it be much simpler so I can comprehend what is going on?
