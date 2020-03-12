import pandas as pd


def load_input(path):
    return [line.rstrip("\n") for line in open(path, "r")]


def save_output(path, l):
    path = path.replace("input", "output")
    open(path, "w").write("\n".join(l))


def process(file):
    output = []
    lines = load_input(file)
    case_count = int(lines[0].strip())
    # Variable for the current line of the file that we are on. 1 is the
    # position of the first case
    case_line = 1

    # Loop through each of the cases
    for case_no in range(0, case_count):
        print("========= CASE {} / {} ============".format(case_no + 1,
                                                           case_count + 1))
        # The case information
        case_info = lines[case_line]
        no_teams = int(case_info.split(" ")[0])  # Number of teams
        no_logs = int(case_info.split(" ")[1])  # Number of log lines

        log = []
        teams = []

        # Go through each of the log lines
        for log_line in range(0, no_logs):
            # Get the line in the file (current case line, add 1 (for the case
            # info line), add the log line)
            line = lines[log_line + 1 + case_line]
            # Split the line into it's seperate values, then convert each item
            # into an integer and add it to the log list
            log.append(list(map(int, line.split(" "))))

        # Create a new pandas dataframe from the log data
        log = pd.DataFrame(data=log, columns=["timestamp", "team", "problem",
                                              "input", "scored"])

        # Loop through each team
        for team in range(1, no_teams + 1):
            # print("TEAM {}".format(team))
            # Get all of the log lines which correspond to the team that we are
            # looping for and only get lines where they have been scored.
            team_log = log[log["team"] == team][log["scored"] == 1]
            # List for storing which challenges have been scored
            already_scored = []
            team_score = 0  # The team's total score
            team_time = 0  # The team's total time penalty

            # Reverse so that we are looking at newest logs first
            team_log.iloc[::-1]

            # Go through each item in the team log (where we have selected the
            # team and only scored log items)
            for index, row in team_log.iterrows():
                # Skip if the team has gotten all of the available challenges
                # (5 inputs * 5 challenges = 25)
                if len(already_scored) == 25:
                    break

                # Tuple of the current challenge and input
                current_problem = (row["problem"], row["input"])

                if current_problem in already_scored:
                    continue

                # Add to the team's total score. It is multipled by 100 because
                # the first input gains 100 points, second input 200 points
                # and so on...
                team_score += row["input"] * 100
                team_time += row["timestamp"]

                # Add the challenge and input to a list so that it doesn't get
                # scored again
                already_scored.append(current_problem)

            # Add the team's number, score and time penalty to the team list
            teams.append((team, team_score, team_time))

        # Create a new pandas dataframe of all of the teams
        teams = pd.DataFrame(data=teams, columns=["team", "score", "time"])
        # Sort the dataframe by descending score, then if they are the same, by
        # ascending time and if they are the same, ascending team id
        teams = teams.sort_values(["score", "time", "team"],
                                  ascending=[False, True, True])

        # print(teams)

        # Get a normal list of the team ids in order
        final_ranking = list(teams["team"])

        # Add a line to the output file with the case number and the final
        # rankings. The list needs to be converted to a list of strings before
        # the join function can be used.
        output.append("Case #{}: {}".format(case_no + 1,
                                            " ".join(list(
                                                map(str, final_ranking)))))

        # Increment the file line counter by 1 (for the case info line) and
        # then by the number of log lines that there is.
        case_line = case_line + 1 + no_logs
        # print("Moving line on {} lines to {}".format(1 + no_logs, case_line))

    # Save the output into a file
    save_output(file, output)


process("input-scoreboard-607a.txt")
