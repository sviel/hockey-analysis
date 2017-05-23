# hockey-analysis

Every year for the NHL playoffs, about 60 members of my extended family participate in a competition to guess its outcome, i.e. which teams will win at each round.
There are 16 NHL teams in the playoffs.
Participants choose 8 teams in the first round, 4 teams in the second, 2 teams advancing to the final and 1 Stanley Cup winner;
in other words they pick one of 2^15 possible scenarios.
Points are earned for each correct guess, and the winning participant is the one with the most points at the end.
As the playoffs unfold, many family members are interested to know whether they still stand a chance at winning the competition, so I wrote a simple Python analysis program to determine who does.


### To run

```bash
python hockey-analysis.py 201x
```

I include two example files with anonymized participants data `pool_201x.txt` and results data `results_201x.txt` for 2013 and 2017.


### Participants data format

The organizer of the competition provides an Excel spreadsheet, so to create the participants data file each year I export the spreadsheet to txt format, add '$' in front of lines with participants' names, and '#end' at the end
(so that input validation is run on the last block of participants data -- there is probably a more elegant way to do this, but it works)


### Results data format

The results data file first has to specify which NHL teams are competing (16 entries).
This is followed by the playoff results for each round.
A line starting with 'x' signifies that the result is unknown, so possible scenarios exist with either team winning.
For example in `results_2017.txt`, I have only entered the outcome of the first round, with the results of subsequent rounds unspecified:
this results in the outcome of 2^7 = 128 possible scenarios being evaluated.
In contrast, the file `results_2013.txt` is fully specified.
There were 4 winning participants that year.

