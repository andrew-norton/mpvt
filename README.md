# Members of Parliament Voting Trends

MPVT's intention is to provide something similar to FiveThirtyEight's [Does Your Member Of Congress Vote With Or Against Biden?](https://projects.fivethirtyeight.com/biden-congress-votes/) for Canadian politicians. The project is very much in early stages at the moment and doesn't support a concise terminal output let alone a webpage to browse. 

Though, if you've somehow stumbled onto this here Github repository and would like to get some data for yourself here's how you can do that!

## Usage

Before starting, be sure to have both [Python](https://www.python.org/) and the [Requests library](https://github.com/psf/requests) installed.

Download a ZIP of this repository, extract and save it anywhere you'd like. Open up the folder it saved to, right click ```main.py``` and open with Python, then wait for it to do it's thing (could take 30 seconds to 2 minutes). 

After the file has ran it's course, you can return back to the folder it saved to and navigate to ```data/member_summaries.csv```. Open this up with Excel or any text editor you'd like. The first half-dozen columns show information relating to the Member of Parliament (eg. their party, riding, province, etc.). Columns H through L show the ratio of election votes received for each party in their riding excluding any votes for parties that did not win seats in the House of Commons (listed in alphabetical order). Columns M through Q show lists of three numbers for each party (again, alphabetical): first is the number of house votes you'd expect that member to agree on with that party, second is the number of votes they actually agreed with each other on, and third is the total number of votes that the member participated in.

## Acknowledgments

That's about all there is to it. Much more to come. Thanks!