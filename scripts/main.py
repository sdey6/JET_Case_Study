from scripts.xkcd_helper import check_table_status, get_latest_comic_id, fetch_xkcd_comic, insert_xkcd_comic
import time


def run_xkcd_process():
    last_id = check_table_status()
    latest_comic_id = get_latest_comic_id()

    if not latest_comic_id:
        print("Failed to get the latest comic ID.")
        return

    print(f"Fetching comics from {last_id + 1} to {latest_comic_id}.\n")

    for comic_id in range(last_id + 1, latest_comic_id + 1):
        comic = fetch_xkcd_comic(comic_id)
        if comic:
            insert_xkcd_comic(comic)
            print(f"Inserted comic with id {comic_id} in the DB")
        time.sleep(0.2)

#
# if __name__ == "__main__":
#     run_xkcd_process()
