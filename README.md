Web map with needed locations
Information about purpose of the module.
	This module defines coordinates of all locations, where films were shot during the year, that was written by user. It finds the city by coordinates written by user and then chooses locations that are closest to it.
	Module returns a web-map with three layers:
		1. The main layer with location of user.
		2. The layer with closest locations, where films were shot during needed year.
		3. The layer with 5 biggest cities in Europe.

2. Structure of an html document:
	html document is divided into two parts:
	- head: it contains all the information about html document (Meta Data, version of html document and style)
	-body: it contains everything that will be displayed on the web page.

	<!DOCTYPE> - defines the type of documents.
	<head> - defines the whole information about the document.
	<meta> - defines metadata about html document.
	<style> - defines style for html document; here you specify how html document will render in a browser.
	<link> - connects document and external resource.
	<body> - defines the body of document; it contains all the contents of this document (text, images, tables, etc.)
	<div> - defines a section in html document.

3. Conclusion about information given us by this map.
	This we map illustrates us the closest locations of films that were shot during the needed year.
	Besides, it also shows us top 5 biggest cities of Europe.
	Doing this task i learned how to use new libraries and make html documents.

4. The result of launching.
    Please enter a year you would like to have a map for: 2004
    Please enter your location (format: lat, long): 69.1221, 20.31231
    Map is generating...
    Please wait...
    ![](example_1.png)

    Please enter a year you would like to have a map for: 2000
    Please enter your location (format: lat, long): 49.3123, 2.3200
    Map is generating...
    Please wait...
    Finished. Please have look on the map Map_1.html
    ![](example_2.png)