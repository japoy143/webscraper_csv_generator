import pandas as pd
import utils.action as sc


quit = False
url = input("please provide website url:")
html_data = []

df = pd.DataFrame(columns=[])
actions = sc.WebscrapingActions
savable = False
indexes = ""
while not quit:
    actions.printStatement(0)

    if savable:
        actions.printStatement(5)

    # action 'c-continue', 'c-clear', 'q-quit'
    action = input("please provide action: ")

    if action.lower().strip() == "cr":
        action = input(
            "provide column name, column name must be separated in comma ex:People,Student : "
        )

        try:
            split_data = action.split(",")
            df = pd.DataFrame(columns=split_data)
            print(df)
        except Exception as e:
            print(f"error occurred {e}")

    if action.lower().strip() == "s" and savable:
        action = input("please provide csv name: ")
        df.to_csv(f"csv_files/{action}.csv", index=False)
        print("successfully saved csv file")
        break

    if action.lower().strip() == "q":
        break
    elif action.lower().strip() == "cl":
        actions.clearLogs(10)
        continue
    else:
        try:
            html_data = actions.showData(url)
            actions.clearLogs(5)
        except Exception as e:
            print(f"error occurred {e}")

        # action sc-scrape html tag
        actions.printStatement(1)
        action = input("please provide action: ")
        if action.lower().strip() != "sc":
            continue

        quitScraping = False

        while not quitScraping:
            action = input("please provide htmltag ex:body,table,th,tr,td: ")
            # scrape html tag
            try:
                html_data = actions.scrapeHtmlTag(html_data, action)
            except Exception as e:
                html_data = actions.showData(url)
                print(f"error encountered skipped:{e}")
                continue

            # action 'c-continue scraping', 'g-get html text' 'provide index number'
            actions.printStatement(2)
            action = input("please provide action: ")

            if action.lower().strip() == "g":
                quitScraping = True

            if action.isdigit():
                index = int(action)

                html_data = html_data[index]
                actions.clearLogs(40)
                print("here")
                print(html_data)
                actions.clearLogs(10)
                quitScraping = True

            if action.lower().strip() == "c":
                try:
                    html_data = actions.showData(url)
                    actions.clearLogs(10)
                except Exception as e:
                    print(f"error occurred {e}")
        try:
            html_data = actions.getHtmlText(html_data)
        except Exception as e:
            print(f"error occurred {e}")
            continue

        # action 'g-to get data', 'get the item from index start-end ex:0-9: '
        actions.printStatement(3)
        action = input("please provider action: ")
        indexes = action

        if action.lower() == "g":
            continue

        actions.clearLogs(10)

        try:
            html_data = actions.getIndexesData(action, html_data)
        except Exception as e:
            print(f"error occurred {e}")
            continue

        # action save as column data  or save as row data
        actions.printStatement(4)
        action = input("please provider action: ")

        if action.lower().strip() == "cd":
            df = pd.DataFrame(columns=html_data)
            print(df)

        if action.lower().strip() == "rd":
            positions = [int(num) for num in indexes if num.isdigit()]
            expected_length = len(df.columns)

            if actions.is_2d_array(html_data):
                for item in html_data:
                    # Trim or pad to match DataFrame column length
                    fixed_item = item[:expected_length]
                    fixed_item += [None] * (expected_length - len(fixed_item))
                    df.loc[len(df)] = fixed_item
            else:
                for item in html_data:
                    length = len(df)
                    df.loc[length] = item

            savable = True
            print(df)
            continue
