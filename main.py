import os
import matplotlib.pyplot as plt
import numpy as np

from api import API

# Check api.py for valid game_name values
def plot_tournament(api_key, tournament_slug, game_name):
    smashgg_api = API(api_key)
    results = smashgg_api.get_tournament(tournament_slug, game_name)

    for key in results:
        event = results[key]
        if "Singles" not in event["event_name"]:
            continue
        y = []
        x = []
        n = []

        for standing in event["standings"]:
            y.append(standing["performance"])
            x.append(standing["placement"])
            n.append(standing["name"])

        existing = {}

        for index in range(0, len(y)):
            cur_x = x[index]
            cur_y = y[index]
            cur_n = n[index]

            if cur_x not in existing:
                existing[cur_x] = {}

            if cur_y not in existing[cur_x]:
                existing[cur_x][cur_y] = []

            existing[cur_x][cur_y].append(cur_n)

        final_y = []
        final_x = []
        final_n = []

        for key in existing:
            for temp_y in existing[key]:
                final_x.append(key)
                final_y.append(temp_y)
                final_n.append(existing[key][temp_y])

        fig, ax = plt.subplots()

        plt.title(f"{event['tournament_name']} - {event['event_name']}")
        plt.yticks(range(-10, 10))
        plt.xlabel("placement")
        plt.ylabel("seed performance")

        ax.scatter(np.array(final_x).astype('str'), final_y)
        for i, txt in enumerate(final_n):
            if len(txt) < 2:
                caption = ','.join(txt)
            else:
                caption = f"{len(txt)} players"

            ax.annotate(caption, (str(final_x[i]), final_y[i] + 0.1))

        ax.set_xlabel("placement")
        ax.set_ylabel("seed performance")


if __name__ == '__main__':
    token = os.environ["SMASHGG_TOKEN"]
    for slug in [
        "battle-of-bc-4-2"
    ]:
        plot_tournament(token, slug, "ultimate")
    plt.show()
