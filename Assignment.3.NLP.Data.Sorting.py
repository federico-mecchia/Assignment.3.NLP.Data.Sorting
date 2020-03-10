"""
Assignment 3 - NLP Data Sorting
"""


import re
import pandas as pd
from textblob import TextBlob


def remove_duplicates_lines(input_file_name, output_file_name):

    curr_check_input_file = open(input_file_name, "r")
    output_file = open(output_file_name, "w")
    list_lines = []

    for line in curr_check_input_file:
        if line in list_lines:
            continue
        else:
            output_file.write(line)
            list_lines.append(line)
    output_file.close()
    curr_check_input_file.close()


def read_write_file_by_regex(input_file_name, input_file_name_regex, output_file_name):

    successful_match_index = 0
    success = 0
    curr_input_file_object = open(input_file_name, "r")
    curr_output_file_object = open(output_file_name, "a+")
    curr_input_file_contents = curr_input_file_object.read()
    curr_match_obj = re.match(input_file_name_regex, curr_input_file_contents)

    if curr_match_obj:
        found_values = re.findall(
            input_file_name_regex, curr_input_file_contents, re.MULTILINE
        )
        if len(found_values) == 50:
            for found_value in found_values:
                successful_match_index = successful_match_index + 1
                curr_output_file_object.write(
                    found_value[0] + "||" + found_value[1] + "\n"
                )
            success = 1
    curr_input_file_object.close()
    curr_output_file_object.close()
    return success


def update_sentiment_value(input_file_name):

    df_sentiment = pd.DataFrame(columns=["Name", "Purpose", "Polarity", "Subjectivity"])
    curr_polarity = 0
    curr_subjectivity = 0

    with open(input_file_name, "r") as curr_input_file:
        for line in curr_input_file.readlines():
            name, purpose = line.strip().split("||")
            curr_polarity = TextBlob(purpose).sentiment.polarity
            curr_subjectivity = TextBlob(purpose).sentiment.subjectivity
            df_sentiment = df_sentiment.append(
                {
                    "Name": name,
                    "Purpose": purpose,
                    "Polarity": curr_polarity,
                    "Subjectivity": curr_subjectivity,
                },
                ignore_index=True,
            )

    df_sentiment.to_csv(
        "Output_file_no_duplicates_sentiment_not_sorted_all.txt", sep="\t"
    )

    # Sort data-frame by polarity value
    df_sentiment_sorted = df_sentiment.sort_values(by=["Polarity"], ascending=[False])
    df_sentiment_sorted.to_csv(
        "Output_file_no_duplicates_sentiment_sorted_all.txt", sep="\t"
    )

    # Get top 10 companies by polarity values
    df_sentiment_top_10 = df_sentiment.sort_values(
        by=["Polarity"], ascending=[False]
    ).head(10)
    df_sentiment_top_10.to_csv(
        "Output_file_no_duplicates_sentiment_sorted_top10_details.txt", sep="\t"
    )
    df_sentiment_top_10.to_html(
        "Output_file_no_duplicates_sentiment_sorted_top10_details.html"
    )
    df_sentiment_top_10.to_csv(
        "Output_file_no_duplicates_sentiment_sorted_top10_names.txt",
        sep="\t",
        columns=["Name"],
    )
    df_sentiment_top_10.to_html(
        "Output_file_no_duplicates_sentiment_sorted_top10_names.html", columns=["Name"]
    )

    # Get bottom 10 companies by polarity values
    df_sentiment_tail_10 = df_sentiment.sort_values(
        by=["Polarity"], ascending=[False]
    ).tail(10)
    df_sentiment_tail_10.to_csv(
        "Output_file_no_duplicates_sentiment_sorted_bottom10_details.txt", sep="\t"
    )
    df_sentiment_tail_10.to_html(
        "Output_file_no_duplicates_sentiment_sorted_bottom10_details.html"
    )
    df_sentiment_tail_10.to_csv(
        "Output_file_no_duplicates_sentiment_sorted_bottom10_names.txt",
        sep="\t",
        columns=["Name"],
    )
    df_sentiment_tail_10.to_html(
        "Output_file_no_duplicates_sentiment_sorted_bottom10_names.html",
        columns=["Name"],
    )


def main():

    files_dictionary = {
        "file_1": {
            "file_name": "result.txt",
            "regex": "^Name:\s*(.*)\nPurpose:\s*(.*)",
        },
        "file_2": {
            "file_name": "output_Webscrap_HW2.txt",
            "regex": "^Name:\s*(.*),Purpose:\s*(.*)",
        },
        "file_3": {"file_name": "Company.txt", "regex": "^\d{1,2}\)(.*)\n\s*(.*)"},
        "file_4": {
            "file_name": "595_HW2.txt",
            "regex": "^Name:\s*(.*)\nPurpose:\s*(.*)",
        },
        "file_5": {
            "file_name": "result.csv",
            "regex": '^(?:name,purpose\n)?"?(.*[^"]\\b(?!name\\b)\w+)"?,"?(.*[^"])(\n)',
        },
        "file_6": {
            "file_name": "napu.csv",
            "regex": '^(?:,Name,Purpose\n)?\d{1,2},"?(.*[^"])"?,"?(.*[^"])(\n)',
        },
        "file_7": {
            "file_name": "ListOfCompanies JVansant.csv",
            "regex": '^(?:,Name,Purpose\n)?\d{1,2},"?(.*[^"])"?,"?(.*[^"])(\n)',
        },
        "file_8": {
            "file_name": "companies1.txt",
            "regex": "^(?:Name\s*Purpose\n)?(.*\\b(?!Name\\b)\w+)\\t(.*)",
        },
        "file_9": {
            "file_name": "Company Details.txt",
            "regex": "^(?:Company Details\s*\n)?Name:\s*(.*)\nPurpose:\s*(.*)",
        },
        "file_10": {
            "file_name": "companies.txt",
            "regex": '^(?:,name,purpose\n)?\d{1,2},"?(.*[^"])"?,"?(.*[^"])(?:\n)',
        },
    }

    for k1, v1 in files_dictionary.items():
        if (
            read_write_file_by_regex(
                v1.get("file_name"), v1.get("regex"), "Output_file_all.txt"
            )
            == 1
        ):
            print("All done!")
        else:
            print("Something went wrong")

    remove_duplicates_lines("Output_file_all.txt", "Output_file_no_duplicates.txt")
    update_sentiment_value("Output_file_no_duplicates.txt")


if __name__ == "__main__":
    main()


"""
Comment

I downloaded 10 files from the Discussion Board. Two of the ten files I
downloaded had the same name and, in fact, they were both named
"companies.txt".
For this reason, I renamed one of the two files (the one containing the
"tabs") in "companies1.txt" (I just added a "1"). Therefore, of the ten
files I downloaded, I just renamed one (it was originally named
"companies.txt" and I renamed it in "companies1.txt") and so I did not
rename in any way the other nine files.

First I import "re", I import "pandas" as "pd" and then I also import
"TextBlob" from "textblob".

I define four functions:

"remove_duplicates_lines";
"read_write_file_by_regex";
"update_sentiment_value";
"main".

The first function (named "remove_duplicates_lines") has two arguments:
"input_file_name" and "output_file_name". I then define
"curr_check_input_file" and I set it equal to "open(input_file_name, "r")",
"output_file" and I set it equal to "open(output_file_name, "w")" and also
"list_lines" and I set it equal to "[]". I then create a "for loop" by
including "line" and "curr_check_input_file" and then an "if else loop"
inside the "for loop". Inside the "if else loop" I include
"line in list_lines" after "if", I use "continue" in the following line and
then I include "output_file.write(line)" and "list_lines.append(line)"
after "else". At the end I use ".close" and, in fact, I include
"output_file.close()" and "curr_check_input_file.close()".

The second function (named "read_write_file_by_regex") has three arguments:
"input_file_name", "input_file_name_regex" and "output_file_name". I then
define "successful_match_index" and I set it equal to "0", "success" and I
set it equal to "0", "curr_input_file_object" and I set it equal to
"open(input_file_name, "r")", "curr_output_file_object" and I set it equal
to "open(output_file_name, "a+")", "curr_input_file_contents" and I set it
equal to "curr_input_file_object.read()" and also "curr_match_obj" and I
set it equal to "re.match(input_file_name_regex, curr_input_file_contents)"
(inside the brackets I include both "input_file_name_regex" and
"curr_input_file_contents").
Moreover, I create an "if loop" and I take into consideration
"curr_match_obj". I then define "found_values" and I set it equal to
"re.findall(input_file_name_regex, curr_input_file_contents, re.MULTILINE)"
(inside the brackets I include "input_file_name_regex",
"curr_input_file_contents" and "re.MULTILINE"). Furthermore, I create
another "if loop" and I set "len(found_values)" equal to "50". I then
create inside the "if loop" a "for loop" and I take into consideration
"found_value" and "found_values". Moreover, I set "successful_match_index"
equal to "successful_match_index + 1" and I also use ".write" and, in fact,
I use "curr_output_file_object.write" and I include "found_value[0] + "||" 
+ found_value[1] + "\n"" inside the brackets. I then set "success" equal to
"1". Furthermore, I use ".close" and, in fact, I include
"curr_input_file_object.close()" and also "curr_output_file_object.close()".
Lastly, I also include "return success".

The third function (named "update_sentiment_value") has only one argument:
"input_file_name". I then define "df_sentiment" and I set it equal to
"pd.DataFrame(columns=["Name", "Purpose", "Polarity", "Subjectivity"])"
(inside the brackets I include "Name", "Purpose", "Polarity" and
"Subjectivity"), "curr_polarity" and I set it equal to "0" and also
"curr_subjectivity" and I set it equal to "0". I then use "with" and I
take into consideration "open(input_file_name, "r")" and "curr_input_file".
Moreover, I create a "for loop" and I take into consideration "line" and
"curr_input_file.readlines()". I then define "name, purpose" and I set it
equal to "line.strip().split("||")", "curr_polarity" and I set it equal
to "TextBlob(purpose).sentiment.polarity" and also "curr_subjectivity" and
I set it equal to "TextBlob(purpose).sentiment.subjectivity". Moreover,
I use ".append()" and, in fact, I define "df_sentiment" and I set it equal
to "df_sentiment.append({"Name": name, "Purpose": purpose,
"Polarity": curr_polarity, "Subjectivity": curr_subjectivity,},
ignore_index=True,)". I then use ".to_csv()" to create a file in ".txt format"
named "Output_file_no_duplicates_sentiment_not_sorted_all.txt" (to this
regard I also include "sep="\t"). Furthermore, I use ".sort_values()" to
sort the data by "Polarity" (to this regard, in fact, I include
"by=["Polarity"]" inside the brackets) and I also sort the data from best
to worst (to this regard, in fact, I include "ascending=[False]" inside
the brackets). I then use again ".to_csv()" to create a file in ".txt format"
named "Output_file_no_duplicates_sentiment_sorted_all.txt" (to this
regard I also include "sep="\t"").
Furthermore, I then get the top 10 companies by polarity values and, in fact,
I define "df_sentiment_top_10" and I set it equal to
"df_sentiment.sort_values(by=["Polarity"], ascending=[False]).head(10)" (I
include ".head(10)" to take into consideration the first 10 companies).
I then use ".to_csv()" to create a file in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_top10_details.txt" (to this
regard I also include "sep="\t""); this file contains the top 10 companies
and includes the columns "Name", "Purpose", "Polarity" and "Subjectivity".
Moreover, I also use ".to_html()" to create a file in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_top10_details.html"; this file
also contains the top 10 companies and includes the columns "Name",
"Purpose", "Polarity" and "Subjectivity".
I then use again ".to_csv()" to create a file in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_top10_names.txt" (to this
regard I also include "sep="\t"" and "columns=["Name"]"); therefore
this file contains the top 10 companies and includes the column "Name".
Moreover, I also use ".to_html()" to create a file in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_top10_names.html"; 
Furthermore, I then get the bottom 10 companies by polarity values and,
in fact, I define "df_sentiment_tail_10" and I set it equal to
"df_sentiment.sort_values(by=["Polarity"], ascending=[False]).tail(10)" (I
include ".tail(10)" to take into consideration the last 10 companies).
I then use ".to_csv()" to create a file in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_details.txt" (to this
regard I also include "sep="\t""); this file contains the bottom 10 companies
and includes the columns "Name", "Purpose", "Polarity" and "Subjectivity".
Moreover, I also use ".to_html()" to create a file in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_details.html"; this file
also contains the bottom 10 companies and includes the columns "Name",
"Purpose", "Polarity" and "Subjectivity".
I then use again ".to_csv()" to create a file in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_names.txt" (to this
regard I also include "sep="\t"" and "columns=["Name"]"); therefore
this file contains the bottom 10 companies and includes the column "Name".
Moreover, I also use ".to_html()" to create a file in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_names.html"; this file
also contains the bottom 10 companies and includes the column "Name".


I thus create eight files in total, four files for the top 10 companies
and four files for the bottom 10 companies:


Top 10 companies:

- File in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_top10_details.txt"

This file contains the top 10 companies
and includes the columns "Name", "Purpose", "Polarity" and "Subjectivity"

- File in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_top10_details.html"

This file also contains the top 10 companies and includes the columns "Name",
"Purpose", "Polarity" and "Subjectivity"

- File in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_top10_names.txt"

This file contains the top 10 companies and includes the column "Name"

- File in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_top10_names.html"

This file also contains the top 10 companies and includes the column "Name"


Bottom 10 companies:

- File in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_details.txt"

This file contains the bottom 10 companies and includes the columns
"Name", "Purpose", "Polarity" and "Subjectivity"

- File in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_details.html"

This file also contains the bottom 10 companies and includes the columns "Name",
"Purpose", "Polarity" and "Subjectivity"

- File in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_names.txt"

This file contains the bottom 10 companies and includes the column "Name"

- File in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_names.html"

This file also contains the bottom 10 companies and includes the column "Name"



The fourth function is the "main()" function.
Inside the function I include "files_dictionary" and I set it equal to the ten
files associated to their specific "regex". In other words, I take into
consideration one file at the time and also its "regex"; the purpose of each
"regex" is to take into consideration ("to capture") the information I am
interested in (for instance the names of the companies and the purposes)
that can be found in the specific file taken into consideration.
In this way I capture in total 500 names (50 names for each of the ten files)
and also 50 purposes.
Moreover, I also create a "for loop" and I include "k1", "v1" and
"files_dictionary.items()". I then create an "if else loop" and I include
"read_write_file_by_regex(v1.get("file_name"), 
v1.get("regex"), "Output_file_all.txt") == 1". I then use "print()" to 
print "All done!" or "Something went wrong". Finally, I also include
"remove_duplicates_lines("Output_file_all.txt", 
"Output_file_no_duplicates.txt")" (inside the brackets I include both
"Output_file_all.txt" and "Output_file_no_duplicates.txt") and also
"update_sentiment_value("Output_file_no_duplicates.txt")" (inside the
brackets I include only "Output_file_no_duplicates.txt").

Furthermore, I also use "if __name__ == "__main__":" and I include "main()".

Lastly, I type "black" in the terminal followed by the path of the
file in ".py format" in order to format the whole code contained in the
file taken into consideration (basically the code of the file you are
reading and so the code of the file in ".py format" named
"Assignment.3.NLP.Data.Sorting").



I upload on "Github" the following files:

- File in ".py format" named "Assignment.3.NLP.Data.Sorting" (basically the
file you are reading)

The four files of the top 10 companies:

- File in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_top10_details.txt"

This file contains the top 10 companies
and includes the columns "Name", "Purpose", "Polarity" and "Subjectivity"

- File in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_top10_details.html"

This file also contains the top 10 companies and includes the columns "Name",
"Purpose", "Polarity" and "Subjectivity".

- File in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_top10_names.txt"

This file contains the top 10 companies and includes the column "Name"

The four files of the bottom 10 companies:

- File in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_details.txt"

This file contains the bottom 10 companies and includes the columns
"Name", "Purpose", "Polarity" and "Subjectivity"

- File in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_details.html"

This file also contains the bottom 10 companies and includes the columns "Name",
"Purpose", "Polarity" and "Subjectivity".

- File in ".txt format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_names.txt"

This file contains the bottom 10 companies and includes the column "Name".

- File in ".html format" named
"Output_file_no_duplicates_sentiment_sorted_bottom10_names.html"

This file also contains the bottom 10 companies and includes the column "Name"

The four files that are created when the code is run:

- File in ".txt format" named "Output_file_all"

- File in ".txt format" named "Output_file_no_duplicates"

- File in ".txt format" named
"Output_file_no_duplicates_sentiment_not_sorted_all"

- File in ".txt format" named "Output_file_no_duplicates_sentiment_sorted_all"



For the first part, when I had to clean the data and put it into a standard
form, I noticed that the 10 files all contained data in different formats and
so, for this reason, I had to write a specific "regex" for each file I took
into consideration.
Moreover, the merged file (that contains 500 companies and 500 purposes) did
not have any duplicate; in other words all the "Name - Purpose" were unique.
Lastly, the top 10 companies all have a positive value of "Polarity", while
the bottom 10 companies all have negative values of "Polarity".

"""
