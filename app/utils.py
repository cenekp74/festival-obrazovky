from time import sleep

def reset_reload_file_in_60s():
    sleep(60)
    with open("instance/reload.txt", "w") as f:
        f.write("0")