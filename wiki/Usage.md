# Usage
- [Standard usage](#standard-usage)
- [Search](#search)
- [Get person's history](#get-persons-history)
- [Get current profiles](#get-current-profiles)
- [Change output file](#change-output-file)

## Prerequisite setup
There are a few things that need to be done before running the scraper.
1. Ensure that your connection is protected by a VPN
2. Open a console while in the project folder.

<img src="https://github.com/steveharwell1/profile-scanner/assets/3698156/3570d928-fe9e-438a-bf87-fa324a37142a" width=200/>

3. Ensure that your libraries are loaded. Execute `source venv/bin/activate`. You should see the text `(venv)` appear on your command line.
<img width="699" alt="Screenshot 2023-11-26 at 11 14 55 AM" src="https://github.com/steveharwell1/profile-scanner/assets/3698156/ac688af4-afdc-4832-8638-25bf2be38d42">


## Standard usage
To run the standard scan where new profiles are automatically found and old profile snapshots are periodically refreshed.
If you are starting a new database of profiles the scanner may not know where to start. You can use the search feature to get some initial profiles in the database.

Execute `python scanner`

## Search
The search feature will run a standard topic search on the site. All profile links will be recorded for future scanning.

Execute `python scanner -s "search text"` where you can choose the search text you like.

## Get person's history
Get an excel file of a single person's profile timeline. Each row will be a snapshot of this person's profile.
The person's id must include `https` all the way to the closing `/` as in `https://www.linkedin.com/in/personsid/`

Execute `python scanner -g "profile_link"`

## Get current profiles
Get an excel file of the most recent snapshot for each alumni. Each row will be a different person.

Execute `python scanner -c`

## Change output file
You can modify the output filename by adding on the `-o` flag to the commands that do file output.
The provided filename must end in `.xlsx`.

Example usage `python scanner -c -o my-file-name.xlsx`

