from requests import get

def main(schema, host):
    res = get("{}://{}/".format(schema, host))
    if res.status_code == 200:
        print("Success")
        exit(0)
    else:
        print("Non-200 exit code")
        exit(1)

if __name__ == "__main__":
    main(schema="http", host="localhost:5000")