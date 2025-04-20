from bs4 import BeautifulSoup
import requests


class WebscrapingActions:

    statement = [
        [
            "press c-continue",
            "press cl-clear",
            "press q-quit",
            "press cr to create column",
        ],
        ["press sc-scrape html tag"],
        ["press c-continue scraping", "press g-get html list", "provide index number"],
        [
            "press g-to get data",
            "enter number the item from index start-end ex:0-9 or ex:[0:8][last_index:skip_index]: ",
        ],
        ["press cd to save as column data ", " press rd to save as row data"],
        [
            "press c-continue",
            "press cl-clear",
            "press q-quit",
            "press s to save as csv",
        ],
    ]

    # print statement and logs
    def printStatement(index):
        for sentence in WebscrapingActions.statement[index]:
            print(sentence)

    # clear print logs
    def clearLogs(numLines):
        for line in range(numLines):
            print("")

    # show html data
    def showData(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        # clear logs before printing data
        WebscrapingActions.clearLogs(10)
        # print html data
        print(soup)
        return soup

    # scrape specific html tag
    def scrapeHtmlTag(soup, html_tag):

        html_data = soup.find_all(html_tag)
        WebscrapingActions.clearLogs(10)

        print(html_data)
        return html_data

    # traverse html data and get html text
    def getHtmlText(data):
        cleaned_list = [item for item in data if item != ""]
        print(cleaned_list)
        temp_data = [item.text.strip() for item in cleaned_list]
        remove_newblank = []

        for item in temp_data:
            split_item = item.split("\n")
            all_data = [var for var in split_item if var.strip()]
            remove_newblank.append(all_data)

        flattened_data = [
            item for sublist in remove_newblank for item in sublist if item
        ]

        WebscrapingActions.clearLogs(5)
        print(flattened_data)

        return flattened_data

    def getIndexesData(indexes, html_data):
        # loop and get indexes from start to end

        positions = [int(num) for num in indexes if num.isdigit()]

        final_position = [0, 0] if len(positions) < 2 else positions
        start = final_position[0]
        end = final_position[1]
        skip_index = 0
        last_index = 0
        data = []
        if ":" in indexes:
            last_index = (
                final_position[2] if len(final_position) == 3 else len(html_data)
            )

            skip_index = final_position[3]

            data = [
                html_data[i : i + end] for i in range(0, last_index, end + skip_index)
            ]

            print(data)
            return data

        if final_position == [0, 0]:
            print(html_data)
            return html_data
        else:
            print(html_data[start:end])
            return html_data[start:end]

    def is_2d_array(data):
        return isinstance(data, (list, tuple)) and all(
            isinstance(row, (list, tuple)) for row in data
        )
