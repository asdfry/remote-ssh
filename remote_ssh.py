import argparse
import paramiko
import threading


class ServerThread(threading.Thread):
    def __init__(self, hostname, username, command, password=None, key_filename=None):
        threading.Thread.__init__(self)
        self.hostname = hostname
        self.username = username
        self.command = command
        self.password = password
        self.key_filename = key_filename

    def run(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                key_filename=self.key_filename,
            )
            stdin, stdout, stderr = client.exec_command(self.command)
            stdout.channel.set_combine_stderr(True)
            output = stdout.readlines()
            print(f"Output from {self.hostname}:\n{''.join(output)}")
        except Exception as e:
            print(f"Connection Failed for {self.hostname}: {e}")
        finally:
            client.close()


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", type=str, required=True)
parser.add_argument("-c", "--command", type=str, required=True)
parser.add_argument("-p", "--password", type=str, default=None)
parser.add_argument("-k", "--key_filename", type=str, default=None)
args = parser.parse_args()

with open("servers.txt", "r") as f:
    lines = [i.strip() for i in f.readlines() if not i[0] == "#"]

threads = []

for line in lines:
    thread = ServerThread(
        hostname=line,
        username=args.username,
        command=args.command,
        password=args.password,
        key_filename=args.key_filename,
    )
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()
