# reCaptchaSolver

A project that I worked on over my Christmas 2020 break as a way to learn about web scraping and impove my Python & Selenium skills.

The script is able too circumnavigate Google's reCaptcha using the following steps:
* Open up the target url and navigate to the reCaptcha <iframe>
* Navigate through to the audio challenge and pull in the audio challenge file
* Open a new tab and upload the audio file and convert to text
* Move back to the initial tab and enter the solution 
