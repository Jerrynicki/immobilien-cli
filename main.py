import requests
import sys

mode = sys.argv[1]
if mode != "--help":
    link = sys.argv[2]
    extra_args = sys.argv[3:]
    host = "leo.immobilien"
else:
    extra_args = []

def shorten(link):
    response = requests.post("https://" + host + "/api/create", json={"url": link})
    response = response.json()

    if response["status"] == "success":
        print("https://" + host + "/" + response["urlKey"])
    else:
        print("Error: " + response["status"])

def get(link, link_only, method):
    if link.startswith("http"):
        link = "/".join(link.split("/")[3:])

    if method == "api":
        response = requests.get("https://" + host + "/api/get", json={"urlKey": link})
        response = response.json()

        if response["status"] == "success":
            if link_only:
                print(response["link"])
            else:
                print("Link: " + response["link"], "\nViews: " + str(response["views"]))
        else:
            print("Error: " + response["status"])

    if method == "force":
        response = requests.get("https://" + host + "/" + link, allow_redirects=False)
        print(response.headers.get("location"))

if "--override-host" in extra_args:
    host = extra_args[extra_args.index("--override-host") + 1]

if mode == "-s" or mode == "--shorten":
    shorten(link)

elif mode == "-r" or mode == "--resolve":
    try:
        if "--link-only" in extra_args:
            get(link, True, "api")
        else:
            get(link, False, "api")
    except IndexError:
        get(link, False, "api")

elif mode == "-rf" or mode == "--resolve-force":
    try:
        if "--link-only" in extra_args:
            get(link, True, "force")
        else:
            get(link, False, "force")
    except IndexError:
        get(link, False, "force")


elif mode == "--help":
    print(open("help", "r").read())

else:
    print("Invalid arguments. Try --help for help.")
