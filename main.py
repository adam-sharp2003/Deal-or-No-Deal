from datetime import datetime
import csv, random, math, os, glob
gamemode = "a"
gmName = "Default"
def addnew(pname): #checks if name is in the playertable
    names = []
    with open(f"csv/players{gmName}.csv", mode="r+", newline="", encoding="utf-8") as playertable:
        for row in csv.reader(playertable): names.append(row[0])
        while pname in names: pname = input("Name already in Leaderboard\nEnter new name: ")
        csv.writer(playertable).writerow([pname, 0])
    return pname
def main():
    global gamemode
    global gmName
    choice = input("""
                         Deal Or No Deal
-------------------------------------------------------------------
                          A: Start game
                          B: Add player
                       C: View game history
  D: Reset All Data (Deletes all players, history, and gamemodes)
                         E: Custom Games
                            Q: Quit
-------------------------------------------------------------------
Please enter your choice: """)
    if choice.lower() == "a":
        leaderboard, num_rows = [[],[]], 0
        with open(f"csv/players{gmName}.csv", mode="r", newline="", encoding="utf-8") as playertable: #prints leaderboard
            header = next(csv.reader(playertable))
            print(f"{header[0]}\t{header[1]}")
            for row in csv.reader(playertable):
                leaderboard[0].append(row[0])
                leaderboard[1].append(int(row[1])) #needs to be int for the comparison
                num_rows += 1
        if num_rows > 1: leaderboard[0], leaderboard[1] = zip(*sorted(list(zip(list(leaderboard[0]),list(leaderboard[1]))),key=lambda x: x[1], reverse=True)) #creates names and scores lists. the lambda sorts the list by the scores instead of the names
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
            for row in csv.reader(open("csv/gamemodes.csv", newline="", encoding="utf-8")):
                if row[0] == gamemode:
                    intboxes = [float(x) for x in row[1:-2]]
                    places = int(row[-2])
            length, rounds, listnum = len(intboxes)-2, [3 for n in range(len(intboxes))], []
            rounds.insert(0, 5)
            for n in range(len(rounds)):
                listnum.append(length if length <= rounds[n] else rounds[n])
                length-=length if length <= rounds[n] else listnum[n]
            opened, nums, rounds, popened = ["Unopened" for n in range(0, len(intboxes))], [*range(1,len(intboxes)+1)], {key:val for key, val in dict(list(enumerate(listnum, 1))).items() if val != 0}, []
            random.shuffle(intboxes)
            boxes, boxesLeft = ["£{:,.2f}".format(m) for m in intboxes], len(intboxes) #creates the string versions
            for n in range(int(len(intboxes)/2)+(1 if len(intboxes)%2 != 0 else 0)):
                print(f"{nums[n]}: {opened[n]}\t{nums[int(n+len(intboxes)/2)]}: {opened[int(n+len(intboxes)/2)]}" if boxesLeft != 1 else f"\t{nums[int(n+len(intboxes)/2)]}: {opened[int(n+len(intboxes)/2)]}") #list of boxes
                boxesLeft -= 2
            pbnum = input("Choose your box: ")
            while pbnum.isdigit() is False or int(pbnum) not in nums: pbnum = input("Choose a valid box: ")
            pbox, pboxint, opened[int(pbnum)-1], pround, dealmade = intboxes[int(pbnum)-1], intboxes[int(pbnum)-1], "Selected", 1, 0
            while pround <= len(rounds) and dealmade == 0:
                choice = 1
                print(f"Round {pround}\nYou will open {rounds[pround]} boxes")
                while choice <= rounds[pround]:
                    popen = input("Choose a box to open: ")
                    while popen.isdigit() is False or popen == pbnum or int(popen) in popened or int(popen) not in nums: popen = input("Choose a box which is valid, unopened and not selected: ")
                    popened.append(int(popen))
                    opened[int(popen)-1], intboxes[int(popen)-1], boxesLeft = boxes[int(popen)-1], 0, len(intboxes)
                    for n in range(int(len(intboxes)/2)+(1 if len(intboxes)%2 != 0 else 0)):
                        print(f"{nums[n]}: {opened[n]}\t{nums[int(n+len(intboxes)/2)]}: {opened[int(n+len(intboxes)/2)]}" if boxesLeft != 1 else f"\t{nums[int(n+len(intboxes)/2)]}: {opened[int(n+len(intboxes)/2)]}") #list of boxes
                        boxesLeft -= 2
                    choice +=1
                bankoffer = 0
                for n in range(len(intboxes)): bankoffer += intboxes[n]**2
                bankoffer = round(math.sqrt(bankoffer/(len(intboxes)-intboxes.count(0)))/places)*places
                deal = input("The Banker has called.\nHe offers £{:,}.\nDeal or No Deal? (d/n): ".format(bankoffer))
                while deal not in ("d","n"): deal = input("Enter either d/n: ")
                if deal == "n": print("The game continues.")
                else: dealmade = 1
                pround +=1
            print("The Final Box had £{:,.2f}. ".format(sum(intboxes)-pboxint) +"\nYour box has £{:,.2f}".format(pbox))
            if dealmade == 0: bankoffer = pbox
            print("You won £{:,.2f}".format(bankoffer))
            if leaderboard[1][leaderboard[0].index(player)] <= bankoffer:
                leaderboard[1][leaderboard[0].index(player)] = bankoffer
                print("Personal High Score!")
            again = input("Play again? (y/n) ")
            while again not in ("y", "n"): again = input("Play again? (y/n) ")
        with open(f"csv/players{gmName}.csv", mode="w+", newline="", encoding="utf-8") as playertable:
            csv.writer(playertable).writerow(["Player Name","High Score"])
            for i in range(len(leaderboard[0])): csv.writer(playertable).writerow([leaderboard[0][i],leaderboard[1][i]])
        csv.writer(open("csv/history.csv", mode="a", newline="", encoding="utf-8")).writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"), player, bankoffer])
    elif choice.lower() == "b": addnew(input("What is the player's name? "))
    elif choice.lower() == "c":
        for row in csv.reader(open("csv/history.csv", newline="", encoding="utf-8"), delimiter=',', quotechar='|'): print(f"{row[0]}\t{row[1]}{': £' if row[2] != ' ' else ' '}{row[2]}")
    elif choice.lower() == "d":
        if input("Are you sure? (y/n) ").lower() == "y":
            for filename in glob.glob("csv/players*"):
                os.remove(filename) 
            csv.writer(open(f"csv/playersDefault.csv", mode="w", newline="", encoding="utf-8")).writerow(["Player Name","High Score"])
            csv.writer(open("csv/history.csv", mode="w", newline="", encoding="utf-8")).writerow(["Date","\t\tScore"," "])
            csv.writer(open("csv/gamemodes.csv", mode="w", newline="", encoding="utf-8")).writerow(["a",0.01,0.10,0.50,1,5,10,50,100,250,500,400,500,750,1000,3000,5000,10000,15000,20000,35000,50000,75000,100000,250000,100,"Default"])
            
            gamemode = "a"
            print("\nLeaderboard RESET")
        else: print("\nLeaderboard NOT RESET")
    elif choice.lower() == "e":
        gamemodes,alphabet = {}, next(csv.reader(open("csv/alphabet.csv", newline="", encoding="utf-8")))
        for row in csv.reader(open("csv/gamemodes.csv", newline="", encoding="utf-8")):
            print(f"{row[0].upper()}: {row[-1]}")
            gamemodes[row[0]] = row[-1]
        gamemode = input(f"{alphabet[len(gamemodes)].upper()}: New\nSelect Game Mode:")
        if gamemode.lower() == alphabet[len(gamemodes)]:
            money, mend, gmName, place = [], 0 ,input("Gamemode Name? "), 1
            print("Input the prizes (as numbers). Press q when finshed.")
            while mend == 0:
                prize = input()
                if prize == "q":
                    if len(money) < 3: print("Input at least 3 prizes. ")
                    else: mend = 1
                elif prize.isdigit() is False: print("Input a number. ")
                else: money.append(int(prize))
            places = input("How many places do you want the banker to round up by? ")
            while places.isdigit() is False: places = input("Input a number. ")
            for i in range(int(places)-1): place *= 10
            money.insert(0, alphabet[len(gamemodes)])
            money.extend([place, gmName])
            csv.writer(open("csv/gamemodes.csv", mode="a", newline="", encoding="utf-8")).writerow(money)
            gamemode = alphabet[len(gamemodes)]
            gamemodes[gamemode] = gmName
            csv.writer(open(f"csv/players{gmName}.csv", mode="a", newline="", encoding="utf-8")).writerow(["Player Name","High Score"])
        else:
            while gamemode.lower() not in gamemodes: gamemode = input("Select a valid gamemode")
        gmName = gamemodes[gamemode]
        return 0
    elif choice.lower() ==  "q": return 1
    else: print("You must only select either A,B,C,D,E, or Q.")
    return 0
if __name__ == '__main__':
    end = 0
    while end == 0: end = main()
