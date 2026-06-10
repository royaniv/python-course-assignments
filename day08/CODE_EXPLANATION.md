# Day 8 Code Explanation

This document explains the Python files in the `day08` folder.

It covers:

- `compound_logic.py`
- `pubchem_amp.py`
- `web_app.py`
- `test_pubchem_amp.py`
- `test_web_app.py`

Blank lines in the code are used only to separate sections and make the code easier to read.

## `compound_logic.py`

This file contains the shared business logic. Both the plot script and the web app use these functions.

| Line | Explanation |
| --- | --- |
| 1 | Imports `Path`, which helps work with file paths such as `compound_list.txt`. |
| 2 | Imports `quote`, which makes compound names safe to place inside a URL. |
| 4 | Imports the `requests` library, which sends HTTP requests to PubChem. |
| 7 | Defines the function `load_compound_list`. If no file name is given, it looks for `compound_list.txt`. |
| 8 | Builds the path to `compound_list.txt` in the same folder as this Python file. |
| 10 | Checks whether that text file actually exists. |
| 11 | Opens the file for reading using UTF-8 text encoding. |
| 12 | Reads every non-empty line, removes extra spaces/newlines, and saves the names in a list. |
| 14 | Checks whether the file produced at least one compound name. |
| 15 | Returns the names from the file. These names are used for the dropdown menu. |
| 17 | If the file is missing or empty, returns an empty list. There is no second hard-coded list inside the Python code. |
| 20 | Defines `get_compound_names`, which turns typed text into a list of compound names. |
| 21 | Checks whether the input text is `None`. |
| 22 | If there is no text, returns an empty list. |
| 24 | Replaces commas with new lines, so both comma-separated and line-separated input work. |
| 25 | Creates an empty list to store the names. |
| 27 | Loops over each line of text. |
| 28 | Removes spaces before and after the current line. |
| 30 | Checks that the line is not empty. |
| 31 | Adds the cleaned compound name to the list. |
| 33 | Returns the final list of typed compound names. |
| 36 | Defines `get_pubchem_data`. It gets TPSA and XLogP for one compound. The `requests_get` argument lets tests use a fake request function. |
| 37 | Starts building the PubChem URL over several lines. |
| 38 | Adds the fixed beginning of the PubChem API URL. |
| 39 | Adds the compound name, using `quote` so spaces and special characters are safe in the URL. |
| 40 | Adds the part of the URL asking PubChem for `XLogP` and `TPSA` in JSON format. |
| 41 | Finishes the multi-line URL expression. |
| 43 | Starts a `try` block. This means Python will try the code inside it, but if one of the listed errors happens, the program will not crash. |
| 44 | Sends the request to PubChem with a 10-second timeout. |
| 45 | Raises an error if PubChem returned a bad HTTP response. |
| 46 | Converts the JSON response into Python dictionaries and lists. |
| 48 | Gets the first properties dictionary from the PubChem response. |
| 50 | Checks that both required values, `TPSA` and `XLogP`, exist. |
| 51 | Starts returning a dictionary for a successful compound. |
| 52 | Stores the compound name. |
| 53 | Stores TPSA as a floating-point number. |
| 54 | Stores XLogP as a floating-point number. |
| 55 | Ends the returned dictionary. |
| 56 | Catches common problems: request failure, missing keys, wrong list index, wrong type, or bad number conversion. |
| 57 | Returns `None` when the compound cannot be used. |
| 59 | Also returns `None` if the response worked but did not contain both required values. |
| 62 | Defines `get_many_compounds`, which processes a list of compounds. |
| 63 | Creates an empty list for compounds that were found successfully. |
| 64 | Creates an empty list for compounds that were skipped. |
| 66 | Loops through every compound name in the input list. |
| 67 | Calls `get_pubchem_data` for the current compound. |
| 69 | Checks whether the result was `None`. |
| 70 | If the result was `None`, adds the compound to the skipped list. |
| 71 | Starts the `else` case for compounds that were found. |
| 72 | Adds the successful compound data dictionary to the found list. |
| 74 | Returns both lists: found compounds first, skipped compounds second. |

## `pubchem_amp.py`

This is the separate plotting script. It makes a matplotlib scatter plot.

| Line | Explanation |
| --- | --- |
| 1 | Imports matplotlib's plotting module and gives it the shorter name `plt`. |
| 3 | Imports the shared functions that load compound names and get PubChem data. |
| 6 | Defines the main function for the script. |
| 7 | Loads the compound names from `compound_list.txt`. |
| 8 | Gets the found and skipped compounds using the shared business logic. |
| 10 | Loops over skipped compounds. |
| 11 | Prints the name of each skipped compound. |
| 13 | Prints how many compounds will be plotted. |
| 15 | Checks whether no compounds were found. |
| 16 | Prints a message saying there is nothing to plot. |
| 17 | Stops the function early if there is no data. |
| 19 | Creates an empty list for TPSA values. |
| 20 | Creates an empty list for XLogP values. |
| 22 | Loops over each successful compound dictionary. |
| 23 | Adds that compound's TPSA value to the TPSA list. |
| 24 | Adds that compound's XLogP value to the XLogP list. |
| 26 | Creates a new matplotlib figure with size 12 by 8 inches. |
| 27 | Draws the scatter plot, using TPSA for x-values and XLogP for y-values. |
| 29 | Loops again over the found compounds to add labels. |
| 30 | Starts a `plt.text` call, which places text on the graph. |
| 31 | Places the label slightly to the right of the compound's TPSA value. |
| 32 | Places the label slightly above the compound's XLogP value. |
| 33 | Uses the compound name as the text label. |
| 34 | Ends the `plt.text` call. |
| 36 | Labels the x-axis and explains that TPSA means topological polar surface area. |
| 37 | Labels the y-axis and explains that XLogP represents the octanol-water partition coefficient. |
| 38 | Adds a title to the plot. |
| 39 | Opens the plot window. |
| 42 | Checks whether the file is being run directly, not imported by another file. |
| 43 | Runs `main()` when the script is run directly. |

## `web_app.py`

This file creates a simple web page using only Python's built-in web server.

### Imports

| Line | Explanation |
| --- | --- |
| 1 | Imports `escape`, which makes text safer to put into HTML. |
| 2 | Imports `BaseHTTPRequestHandler` and `HTTPServer` from Python's built-in web server tools. |
| 3 | Imports `parse_qs` and `urlparse`, which read query parameters from a URL. |
| 5 | Imports the shared business logic functions from `compound_logic.py`. |

### `choose_compound_names`

| Line | Explanation |
| --- | --- |
| 8 | Defines a function that combines selected compounds and typed compounds. |
| 9 | Creates an empty list called `names`. |
| 11 | Checks whether the user selected any compounds from the list. |
| 12 | Loops through each selected compound. |
| 13 | Removes spaces before and after the selected compound name. |
| 15 | Checks that the selected compound name is not empty. |
| 16 | Adds the selected compound name to `names`. |
| 18 | Adds the typed compound names after converting the typed text into a list. |
| 20 | Creates an empty list for unique names only. |
| 22 | Loops through all names. |
| 23 | Checks whether the name is not already in the unique list. |
| 24 | Adds the name if it is new. |
| 26 | Returns the final list without duplicates. |

### `make_plot_svg`

This function creates a simple scatter plot as SVG text. SVG is image markup that the browser can draw.

| Line | Explanation |
| --- | --- |
| 29 | Defines a function that receives found compounds and returns SVG HTML. |
| 30 | Checks if the list is empty. |
| 31 | Returns an empty string if there is nothing to plot. |
| 33 | Creates an empty list for TPSA values. |
| 34 | Creates an empty list for XLogP values. |
| 36 | Loops through every found compound. |
| 37 | Adds the compound's TPSA value to the TPSA list. |
| 38 | Adds the compound's XLogP value to the XLogP list. |
| 40 | Finds the smallest TPSA value. |
| 41 | Finds the largest TPSA value. |
| 42 | Finds the smallest XLogP value. |
| 43 | Finds the largest XLogP value. |
| 45 | Checks whether all TPSA values are the same. |
| 46 | Lowers the minimum TPSA by 1 so the graph has width. |
| 47 | Raises the maximum TPSA by 1 so the graph has width. |
| 49 | Checks whether all XLogP values are the same. |
| 50 | Lowers the minimum XLogP by 1 so the graph has height. |
| 51 | Raises the maximum XLogP by 1 so the graph has height. |
| 53 | Sets the SVG image width in pixels. |
| 54 | Sets the SVG image height in pixels. |
| 55 | Sets the left margin inside the plot. |
| 56 | Sets the right margin inside the plot. |
| 57 | Sets the top margin inside the plot. |
| 58 | Sets the bottom margin inside the plot. |
| 59 | Calculates the actual drawable plot width. |
| 60 | Calculates the actual drawable plot height. |
| 62 | Creates an empty string for the SVG circles. |
| 63 | Creates an empty string for the SVG text labels. |
| 65 | Loops through every compound to calculate its point position. |
| 66 | Converts the compound's TPSA value into an x-coordinate inside the SVG. |
| 67 | Converts the compound's XLogP value into a y-coordinate inside the SVG. |
| 69 | Adds one SVG circle for the compound point. |
| 70 | Starts adding an SVG text label over several lines. |
| 71 | Sets the text label position slightly right and above the point. |
| 72 | Adds the escaped compound name and closes the SVG text element. |
| 73 | Ends the multi-line text-label expression. |
| 75 | Calculates where the x-axis should be drawn. |
| 77 | Starts returning a large formatted HTML/SVG string. |
| 78 | Opens a `div` container for the plot. |
| 79 | Adds the visible heading `Plot`. |
| 80 | Starts the SVG element and sets its coordinate system. |
| 81 | Draws the horizontal x-axis. |
| 82 | Draws the vertical y-axis. |
| 84 | Adds the minimum TPSA tick label. |
| 85 | Adds the maximum TPSA tick label. |
| 86 | Adds the minimum XLogP tick label. |
| 87 | Adds the maximum XLogP tick label. |
| 89 | Inserts all SVG circle points created earlier. |
| 90 | Inserts all SVG text labels created earlier. |
| 92 | Adds the x-axis label and explains TPSA. |
| 93 | Adds the rotated y-axis label and explains XLogP. |
| 94 | Closes the SVG element. |
| 95 | Closes the plot container. |
| 96 | Ends the returned multi-line string. |

### `make_compound_options`

| Line | Explanation |
| --- | --- |
| 99 | Defines a function that creates the `<option>` tags for the dropdown list. |
| 100 | Checks whether no compounds were selected. |
| 101 | Uses an empty selected list if nothing was selected. |
| 103 | Converts the selected compounds to a `set`, which makes checking membership easier. |
| 104 | Creates an empty string for the option HTML. |
| 106 | Loops through every compound from `compound_list.txt`. |
| 107 | Adds the word `selected` to the option if that compound was selected by the user. |
| 108 | Starts adding one option tag over several lines. |
| 109 | Creates the opening `<option>` tag and safely places the compound in the `value`. |
| 110 | Places the visible compound name and closes the option tag. |
| 111 | Ends the multi-line option expression. |
| 113 | Returns all option tags as one string. |

### `make_results_html`

| Line | Explanation |
| --- | --- |
| 116 | Defines a function that builds the results section of the page. |
| 117 | Checks whether no lookup has happened yet. |
| 118 | Returns an empty string so the start page has no results area. |
| 120 | Creates an empty string for table rows. |
| 122 | Loops through each found compound. |
| 123 | Starts adding a table row as a multi-line string. |
| 124 | Opens an HTML table row. |
| 125 | Adds the compound name in a table cell, safely escaped. |
| 126 | Adds the TPSA value in a table cell. |
| 127 | Adds the XLogP value in a table cell. |
| 128 | Closes the table row. |
| 129 | Ends the table-row string. |
| 131 | Creates an empty string for skipped compound names. |
| 133 | Checks whether there are skipped compounds. |
| 134 | Joins skipped names into one comma-separated string. |
| 136 | Checks whether no skipped text was created. |
| 137 | Uses `None` when no compounds were skipped. |
| 139 | Creates the plot HTML/SVG by calling `make_plot_svg`. |
| 141 | Starts returning the full results section. |
| 142 | Opens the results section. |
| 143 | Opens a heading wrapper. |
| 144 | Adds the `Results` heading. |
| 145 | Adds a small count badge showing how many compounds were found. |
| 146 | Closes the heading wrapper. |
| 148 | Adds a sentence giving the number of found compounds. |
| 150 | Opens the table. |
| 151 | Opens the header row. |
| 152 | Adds the `Compound` column heading. |
| 153 | Adds the TPSA column heading and its meaning. |
| 154 | Adds the XLogP column heading and its meaning. |
| 155 | Closes the header row. |
| 156 | Inserts all the table rows created earlier. |
| 157 | Closes the table. |
| 159 | Adds the skipped-compounds line, safely escaping the skipped text. |
| 161 | Inserts the plot HTML/SVG. |
| 162 | Closes the results section. |
| 163 | Ends the returned multi-line string. |

### `make_page`

This function returns the full HTML page. Lines 180-397 are CSS, which means styling rules for the page.

| Line | Explanation |
| --- | --- |
| 166 | Starts the definition of `make_page`. |
| 167 | Receives text typed by the user, defaulting to an empty string. |
| 168 | Receives selected compounds, defaulting to `None`. |
| 169 | Receives found compounds, defaulting to `None`. |
| 170 | Receives skipped compounds, defaulting to `None`. |
| 171 | Ends the function parameter list. |
| 172 | Builds the dropdown option HTML. |
| 173 | Builds the results HTML. |
| 175 | Starts returning the full page as a formatted multi-line string. |
| 176 | Declares the document as HTML. |
| 177 | Opens the HTML document. |
| 178 | Opens the page head. |
| 179 | Sets the browser tab title. |
| 180 | Opens the CSS style block. |
| 181-183 | Applies `box-sizing: border-box` to all elements, making widths easier to control. |
| 185-191 | Styles the whole page body: background color, text color, font, line spacing, and no default margin. |
| 193-197 | Styles `.page` containers: centers content, limits width, and adds padding. |
| 199-204 | Styles the header: dark background, orange bottom border, white text, and padding. |
| 206-210 | Styles the main heading inside the header. |
| 212-217 | Styles the subtitle paragraph inside the header. |
| 219-226 | Styles the form and results panels: white background, border, rounded corners, shadow, spacing, and padding. |
| 228-232 | Creates a two-column grid for the compound list and typed text area. |
| 234-238 | Styles labels above form fields. |
| 240-246 | Gives select boxes and textareas consistent borders, font, and width. |
| 248-251 | Sets the height and padding of the compound select box. |
| 253-257 | Sets the height, padding, and resize behavior of the textarea. |
| 259-263 | Adds a visible focus style when the select box or textarea is active. |
| 265-275 | Styles the submit button. |
| 277-279 | Changes the button color when the mouse hovers over it. |
| 281-287 | Makes the result heading row use flexible spacing. |
| 289-291 | Removes default margin from the `h2` inside the section heading. |
| 293-300 | Styles the small found-count badge. |
| 302-305 | Styles the table so borders collapse and it fills the available width. |
| 307-310 | Styles table header cells. |
| 312-316 | Styles table header and data cells: border, padding, and left alignment. |
| 318-320 | Gives every even table row a slightly different background. |
| 322-325 | Styles small explanatory text inside table headers. |
| 327-330 | Styles the skipped-compounds paragraph. |
| 332-334 | Adds space above the plot area. |
| 336-338 | Styles the plot heading. |
| 340-347 | Styles the SVG plot box: background, border, rounded corners, display, height, and width. |
| 349-352 | Styles the SVG plot axes. |
| 354-358 | Styles the SVG plot points. |
| 360-363 | Styles the SVG point labels and tick labels. |
| 365-369 | Styles the SVG axis labels. |
| 371 | Starts CSS rules that only apply on screens up to 700 pixels wide. |
| 372-374 | Reduces page padding on small screens. |
| 376-378 | Reduces header padding on small screens. |
| 380-382 | Reduces the main heading size on small screens. |
| 384-386 | Changes the form grid from two columns to one column on small screens. |
| 388-390 | Reduces panel padding on small screens. |
| 392-395 | Stacks the results heading and count badge vertically on small screens. |
| 396 | Ends the media-query block. |
| 397 | Closes the CSS style block. |
| 398 | Closes the HTML head. |
| 399 | Opens the body of the page. |
| 400 | Opens the header section. |
| 401 | Opens a centered page container inside the header. |
| 402 | Adds the main page heading. |
| 403 | Adds the subtitle explaining what the app compares. |
| 404 | Closes the header page container. |
| 405 | Closes the header section. |
| 407 | Opens the main content area. |
| 408 | Opens the search panel section. |
| 409 | Opens a form using the `GET` method, so input appears in the URL query string. |
| 410 | Adds a hidden input showing that the form was submitted. |
| 412 | Opens the two-column form grid. |
| 413 | Opens the first form column. |
| 414 | Adds the label for the compound selection box. |
| 415 | Opens the multiple-selection dropdown. |
| 416 | Inserts the generated compound options. |
| 417 | Closes the selection dropdown. |
| 418 | Closes the first form column. |
| 420 | Opens the second form column. |
| 421 | Adds the label for the textarea. |
| 422 | Adds the textarea, including placeholder examples and the current typed text. |
| 423 | Closes the second form column. |
| 424 | Closes the form grid. |
| 426 | Adds the submit button. |
| 427 | Closes the form. |
| 428 | Closes the search panel. |
| 430 | Inserts the results section if a lookup has happened. |
| 431 | Closes the main content area. |
| 432 | Closes the body. |
| 433 | Closes the HTML document. |
| 434 | Ends the returned multi-line page string. |

### `make_page_from_query`

| Line | Explanation |
| --- | --- |
| 437 | Defines a function that receives the query part of a URL. |
| 438 | Parses the query string into a dictionary-like object. |
| 439 | Checks whether the form was submitted. |
| 441 | If the form was not submitted, prepares the empty starting page. |
| 442 | Returns the empty starting page. |
| 444 | Gets the typed compound text from the query. If missing, uses an empty string. |
| 445 | Gets the selected compounds from the query. If missing, uses an empty list. |
| 446 | Combines selected and typed compound names into one list. |
| 447 | Uses the business logic to get found and skipped compounds. |
| 449 | Starts returning the finished page. |
| 450 | Passes the typed compound text to `make_page`. |
| 451 | Passes the selected compounds to `make_page`. |
| 452 | Passes the found compounds to `make_page`. |
| 453 | Passes the skipped compounds to `make_page`. |
| 454 | Ends the `make_page` call. |

### Web Server Class And Startup

| Line | Explanation |
| --- | --- |
| 457 | Defines `AmphiphileHandler`, a class that handles browser requests. |
| 458 | Defines what happens when the browser sends a `GET` request. |
| 459 | Splits the requested URL into parts. |
| 461 | Checks whether the requested path is not `/`. |
| 462 | Sends a 404 error for unknown paths. |
| 463 | Stops handling the request after sending the error. |
| 465 | Builds the HTML page using the query string from the URL. |
| 466 | Converts the HTML text into bytes so it can be sent over HTTP. |
| 468 | Sends HTTP status code 200, meaning success. |
| 469 | Tells the browser the response is UTF-8 HTML. |
| 470 | Tells the browser how many bytes are in the response. |
| 471 | Ends the HTTP headers. |
| 472 | Sends the actual HTML page bytes to the browser. |
| 475 | Defines `run_server`, with default port 8000. |
| 476 | Creates an HTTP server on `127.0.0.1`, which means this computer only. |
| 477 | Prints the local URL for the user to open. |
| 478 | Keeps the server running and listening for browser requests. |
| 481 | Checks whether this file is being run directly. |
| 482 | Starts the server when the file is run directly. |

## `test_pubchem_amp.py`

This file tests the business logic without using the real internet.

| Line | Explanation |
| --- | --- |
| 1 | Imports `requests` so the test can use `requests.RequestException`. |
| 3 | Imports the business logic functions being tested. |
| 6 | Defines a fake response class to imitate a PubChem response. |
| 7 | Defines how to create a `FakeResponse`. |
| 8 | Stores fake JSON data inside the object. |
| 10 | Defines a fake `raise_for_status` method. |
| 11 | Does nothing, meaning the fake response pretends the request succeeded. |
| 13 | Defines a fake `json` method. |
| 14 | Returns the fake data stored in the object. |
| 17 | Defines a test for splitting typed compound text. |
| 18 | Creates text with both a newline and a comma. |
| 20 | Calls `get_compound_names`. |
| 22 | Checks that the text was split into three clean names. |
| 25 | Defines a test for successful PubChem data extraction. |
| 26 | Defines a fake request function. |
| 27-36 | Creates fake PubChem-style data containing both TPSA and XLogP. |
| 38 | Returns that fake data wrapped in a `FakeResponse`. |
| 40 | Calls `get_pubchem_data` using the fake request function. |
| 42-46 | Checks that the result is the expected dictionary. |
| 49 | Defines a test for missing data. |
| 50 | Defines a fake request function. |
| 51-59 | Creates fake PubChem-style data that has TPSA but not XLogP. |
| 61 | Returns that fake data wrapped in a `FakeResponse`. |
| 63 | Calls `get_pubchem_data`. |
| 65 | Checks that missing XLogP causes the result to be `None`. |
| 68 | Defines a test for failed requests. |
| 69 | Defines a fake request function. |
| 70 | Raises a request exception to imitate a network problem. |
| 72 | Calls `get_pubchem_data`. |
| 74 | Checks that request failure returns `None`. |
| 77 | Defines a test for processing multiple compounds. |
| 78 | Defines a fake request function. |
| 79 | Checks whether the requested URL contains the word `missing`. |
| 80 | Returns incomplete fake data for the missing compound. |
| 81 | Starts the case for compounds that are not missing. |
| 82-91 | Creates complete fake data with TPSA and XLogP. |
| 93 | Returns the fake data wrapped in a `FakeResponse`. |
| 95 | Calls `get_many_compounds` for one good compound and one missing compound. |
| 97-103 | Checks that the found list contains only octanol with the expected values. |
| 104 | Checks that the skipped list contains only `missing`. |

## `test_web_app.py`

This file tests the web page functions without starting a real server.

| Line | Explanation |
| --- | --- |
| 1 | Imports the `web_app` file so the tests can call its functions. |
| 4 | Defines a test for combining selected and typed compound names. |
| 5 | Calls `choose_compound_names`. |
| 6 | Passes two selected compounds. |
| 7 | Passes typed text containing `oleic acid` and duplicate `octanol`. |
| 8 | Ends the function call. |
| 10 | Checks that the result combines names and removes the duplicate. |
| 13 | Defines a test for the home page form. |
| 14 | Creates the page HTML. |
| 16 | Checks that the app title appears in the HTML. |
| 17 | Checks that the selection input appears in the HTML. |
| 18 | Checks that the typed-text input appears in the HTML. |
| 21 | Defines a test for the results page. |
| 22 | Starts a fake list of found compounds. |
| 23 | Starts the fake compound dictionary. |
| 24 | Sets the fake compound name. |
| 25 | Sets the fake TPSA value. |
| 26 | Sets the fake XLogP value. |
| 27 | Ends the fake compound dictionary. |
| 28 | Ends the fake found-compounds list. |
| 30 | Calls `make_page` to create a page with results. |
| 31 | Passes typed compound text. |
| 32 | Passes the fake found compounds. |
| 33 | Passes one skipped compound. |
| 34 | Ends the `make_page` call. |
| 36 | Checks that the page says one compound was found. |
| 37 | Checks that the compound name appears. |
| 38 | Checks that the TPSA explanation appears. |
| 39 | Checks that the XLogP explanation appears. |
| 40 | Checks that the skipped compound appears. |
| 41 | Checks that the SVG plot appears. |
| 44 | Defines a test for making a page from a URL query string. |
| 45 | Defines a fake `get_many_compounds` function. |
| 46 | Checks that the web app sends the expected compound names to the business logic. |
| 48 | Starts returning fake found and skipped results. |
| 49 | Starts the fake found-compounds list. |
| 50 | Starts the fake compound dictionary. |
| 51 | Sets the fake compound name. |
| 52 | Sets the fake TPSA value. |
| 53 | Sets the fake XLogP value. |
| 54 | Ends the fake compound dictionary. |
| 55 | Ends the fake found-compounds list. |
| 56 | Returns an empty skipped list. |
| 57 | Ends the returned tuple. |
| 59 | Replaces `web_app.get_many_compounds` with the fake function for this test. |
| 61 | Calls `make_page_from_query`. |
| 62 | Provides the first part of the fake query string. |
| 63 | Provides the second part of the fake query string. |
| 64 | Ends the function call. |
| 66 | Checks that the page says one compound was found. |
| 67 | Checks that the compound name appears. |
| 68 | Checks that the SVG plot appears. |
