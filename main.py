from datetime import datetime
import csv, random, math
def addnew(pname): #checks if name is in the playertable
    names = []
    with open("players.csv", mode="r+", newline="", encoding="utf-8") as playertable:
        for row in csv.reader(playertable): names.append(row[0])
        while pname in names: pname = input("Name already in Leaderboard\nEnter new name: ")
        csv.writer(playertable).writerow([pname, 0])
    return pname
def main():
    choice = input("""
                  Deal Or No Deal
------------------------------------------------------
A: Start game
B: Add player
C: View game history
D: Reset Leaderboard (Deletes all players and history)
Q: Quit
------------------------------------------------------
Please enter your choice: """)
    if choice.lower() == "a":
        leaderboard, num_rows = [[],[]], 0
        with open("players.csv", mode="r", newline="", encoding="utf-8") as playertable: #prints leaderboard
            header = next(csv.reader(playertable))
            print(f"{header[0]}\t{header[1]}")
            for row in csv.reader(playertable):
                leaderboard[0].append(row[0])
                leaderboard[1].append(int(row[1])) #needs to be int for the comparison
                num_rows += 1
        if num_rows > 1: leaderboard[0], leaderboard[1] = zip(*sorted(list(zip(leaderboard[0],leaderboard[1])),key=lambda x: x[1], reverse=True)) #creates names and scores lists. the lambda sorts the list by the scores instead of the names
        for n in range(2): leaderboard[n] = list(leaderboard[n]) 
        for l in range(len(leaderboard[0])): print(leaderboard[0][l] + "\t\t£{:,}".format(leaderboard[1][l]))
        if len(leaderboard[0]) == 0: print("-----------\t-----\n")
        player = 0
        while player == 0: #loops adding player to leaderboard
            player = input("Who will be playing? ")
            if player not in leaderboard[0]:
                if input("Player not in Leaderboard.\nAdd new player? (y/n)") == "y":
                    leaderboard[0].append(addnew(player))
                    leaderboard[1].append(0)
                else: player = 0
        again= "y"
        while again == "y": #loops game
            opened, nums, rounds, popened = ["Unopened" for n in range(0, 24)], [*range(1,25)], {1:5, 2:3, 3:3, 4:3, 5:3, 6:3, 7:2}, [] 
            intboxes = [0.01, 0.10, 0.50, 1, 5, 10, 50, 100, 250, 500, 400, 500, 750, 1000, 3000, 5000, 10000, 15000, 20000, 35000, 50000, 75000, 100000, 250000]
            random.shuffle(intboxes)
            boxes = ["£{:,.2f}".format(m) if m<100 else "£{:,}".format(m) for m in intboxes] #creates the string versions
            for n in range(12): print(f"{nums[n]}: {opened[n]}\t{nums[n+12]}: {opened[n+12]}") #list of boxes
            pbnum = input("Choose your box: ")
            while pbnum.isdigit() is False or int(pbnum) not in nums: pbnum = input("Choose a valid box: ")
            pbox, pboxint, opened[int(pbnum)-1], pround, dealmade = boxes[int(pbnum)-1], intboxes[int(pbnum)-1], "Selected", 1, 0
            while pround <= len(rounds) and dealmade == 0:
                choice = 1
                print(f"Round {pround}\nYou will open {rounds[pround]} boxes")
                while choice <= rounds[pround]:
                    tab, popen = 1, input("Choose a box to open: ")
                    while popen.isdigit() is False or popen == pbnum or int(popen) in popened or int(popen) not in nums: popen = input("Choose a box which is valid, unopened and not selected: ")
                    popened.append(int(popen))
                    opened[int(popen)-1], intboxes[int(popen)-1] = boxes[int(popen)-1], 0
                    for n in range(12): print(f"{nums[n]}: {opened[n]}  \t{nums[n+12]}: {opened[n+12]}")
                    choice +=1
                bankoffer = 0
                for n in range(len(intboxes)): bankoffer += intboxes[n]**2
                bankoffer = round(math.sqrt(bankoffer/(len(intboxes)-intboxes.count(0)))/100)*100
                deal = input("The Banker has called.\nHe offers £{:,}.\nDeal or No Deal? (d/n): ".format(bankoffer))
                while deal not in ("d","n"): deal = input("Enter either d/n: ")
                if deal == "n": print("The game continues.")
                else: dealmade = 1
                pround +=1
            if dealmade == 0:
                print(f"The Final Box had £{sum(intboxes)-pboxint}\nYour box has {pbox}")
                bankoffer = pbox
            print("You won £{:,}".format(bankoffer))
            if leaderboard[1][leaderboard[0].index(player)] <= bankoffer:
                leaderboard[1][leaderboard[0].index(player)] = bankoffer
                print("Personal High Score!")
            again = input("Play again? (y/n) ")
            while again not in ("y", "n"): again = input("Play again? (y/n) ")
        with open("players.csv", mode="w+", newline="", encoding="utf-8") as playertable:
            csv.writer(playertable).writerow(["Player Name","High Score"])
            for i in range(len(leaderboard[0])): csv.writer(playertable).writerow([leaderboard[0][i],leaderboard[1][i]])
        csv.writer(open("history.csv", mode="a", newline="", encoding="utf-8")).writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"), player, bankoffer])
    elif choice.lower() == "b": addnew(input("What is the player's name? "))
    elif choice.lower() == "c":
        for row in csv.reader(open("history.csv", newline="", encoding="utf-8"), delimiter=',', quotechar='|'): print(f"{row[0]}\t{row[1]}{': £' if row[2] != ' ' else ' '}{row[2]}")
    elif choice.lower() == "d":
        if input("Are you sure? (y/n) ").lower() == "y":
            csv.writer(open("players.csv", mode="w", newline="", encoding="utf-8")).writerow(["Player Name","High Score"])
            csv.writer(open("history.csv", mode="w", newline="", encoding="utf-8")).writerow(["Date","\t\tScore"," "])
            print("\nLeaderboard RESET")
        else: print("\nLeaderboard NOT RESET")
    elif choice.lower() ==  "q": return 1
    else: print("You must only select either A,B,C,D, or Q.")
    return 0
if __name__ == '__main__':
    end = 0
    while end == 0: end = main()