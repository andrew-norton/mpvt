import csv
import urllib.request
import xml.etree.ElementTree as ET


VOTES = ET.fromstring(
    urllib.request.urlopen("https://www.ourcommons.ca/members/en/votes/xml").read()
)

votes_recorded = []
with open("data/vote_summaries.csv") as vote_summaries:
    for line in csv.reader(vote_summaries):
        votes_recorded.append(line[0])

for vote in VOTES:
    if vote[3].text not in votes_recorded:
        vote_number = vote[3].text
        vote_subject = vote[4].text
        vote_date = vote[2].text[:10]
        vote_yeas = vote[6].text
        vote_nays = vote[7].text

        individual_votes = ET.fromstring(
            urllib.request.urlopen(
                "https://www.ourcommons.ca/Members/en/votes/44/1/"
                + vote_number
                + "/xml"
            ).read()
        )

        bloc = [0, 0]
        conservative = [0, 0]
        green = [0, 0]
        liberal = [0, 0]
        ndp = [0, 0]

        for person in individual_votes:
            vote_value = person[6].text
            party = person[10].text

            match party:
                case "Bloc Québécois":
                    bloc[1] += 1
                    if vote_value == "Yea":
                        bloc[0] += 1
                case "Conservative":
                    conservative[1] += 1
                    if vote_value == "Yea":
                        conservative[0] += 1
                case "Green Party":
                    green[1] += 1
                    if vote_value == "Yea":
                        green[0] += 1
                case "Liberal":
                    liberal[1] += 1
                    if vote_value == "Yea":
                        liberal[0] += 1
                case "NDP":
                    ndp[1] += 1
                    if vote_value == "Yea":
                        ndp[0] += 1

        bloc, conservative, green, liberal, ndp = (
            numerator / denominator
            for numerator, denominator in [bloc, conservative, green, liberal, ndp]
            if denominator != 0
        )
        # bloc, conservative, green, liberal, ndp = ("N/A" for party in [bloc, conservative, green, liberal, ndp] if isinstance(party, list))

        with open("data/vote_summaries.csv", "a", newline="") as vote_summaries:
            csv.writer(vote_summaries).writerow(
                [
                    vote_number,
                    vote_subject,
                    vote_date,
                    vote_yeas,
                    vote_nays,
                    bloc,
                    conservative,
                    green,
                    liberal,
                    ndp,
                ]
            )

        for person in individual_votes:
            person_id = person[15].text
            vote_value = person[6].text
            yea_probability = 0

            if vote_value == "Yea":
                vote_value = 1
            else:
                vote_value = 0

            with open("data/member_summaries.csv") as member_summaries:
                for member in csv.reader(member_summaries):
                    if member[0] == person_id:
                        file_location = "data/" + member[1]

                        if member[7] != "0":
                            yea_probability += float(member[7]) * bloc
                        if member[8] != "0":
                            yea_probability += float(member[8]) * conservative
                        if member[9] != "0":
                            yea_probability += float(member[9]) * green
                        if member[10] != "0":
                            yea_probability += float(member[10]) * liberal
                        if member[11] != "0":
                            yea_probability += float(member[11]) * ndp

                        with open(file_location, "a", newline="") as member_file:
                            csv.writer(member_file).writerow(
                                [
                                    vote_number,
                                    vote_subject,
                                    vote_date,
                                    vote_yeas,
                                    vote_nays,
                                    round(yea_probability, 2),
                                    vote_value,
                                    round(bloc),
                                    round(conservative),
                                    round(green),
                                    round(liberal),
                                    round(ndp),
                                ]
                            )


updated_member_summaries = []

with open("data/member_summaries.csv") as member_summaries:
    for member in csv.reader(member_summaries):
        file_location = "data/" + member[1]
        bloc, conservative, green, liberal, ndp = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        with open(file_location) as member_file:

            for vote in csv.reader(member_file):

                yea_probability = float(vote[5])
                vote_value = int(vote[6])
                party_column = 7

                for party in (bloc, conservative, green, liberal, ndp):
                    if int(vote[party_column]) == 1:
                        party[0] += yea_probability
                    else:
                        party[0] += 1 - yea_probability
                    if vote_value == int(vote[party_column]):
                        party[1] += 1
                    party[2] += 1
                    party_column += 1

        for party in (bloc, conservative, green, liberal, ndp):
            party[0] = round(party[0], 2)

        member = member[:12]
        member.extend([bloc, conservative, green, liberal, ndp])
        updated_member_summaries.append(member)

with open("data/member_summaries.csv", "w", newline="") as member_summaries:
    for item in updated_member_summaries:
        csv.writer(member_summaries).writerow(item)
