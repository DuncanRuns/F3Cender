import time
import discord_webhook
import clipboard
from threading import Thread
import json
import os

version = "1.0.0"

lisc = """Copyright (c) 2021 DuncanRuns

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""


def isNumber(string: str):
    try:
        float(string)
        return True
    except:
        return False


def isF3C(string: str):
    if string.startswith("/execute in minecraft:overworld run tp @s "):
        args = string.split(" ")
        if len(args) == 11:
            for i in range(6, 11):
                if not isNumber(args[i]):
                    return False
            return True
    return False


class F3Cender:
    def __init__(self, url: str, username: str):
        self.url = url
        self.username = username
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            print("Listening for clipboard...")
            Thread(target=self._loop).start()

    def stop(self):
        self.running = False

    def _sendF3C(self, string: str):
        try:
            print(f"Sending {string}")
            content = self.username + " sent:\n" + string
            discord_webhook.DiscordWebhook(self.url, content=content).execute()
        except:
            print("Error sending clipboard.")

    def _loop(self):
        lastPaste = clipboard.paste()
        while self.running:
            time.sleep(0.2)
            newPaste = clipboard.paste()
            if newPaste != lastPaste:
                lastPaste = newPaste
                if isF3C(newPaste):
                    print("New paste matches f3+c format.")
                    self._sendF3C(newPaste)
                else:
                    print("New paste does not match f3+c format.")


def printInfo():
    print(lisc)
    print("\n---------------------\n")
    print("F3Cender v"+version)
    print("\n---------------------\n")


if __name__ == "__main__":
    printInfo()
    if not os.path.isfile("f3cender.json"):
        print("No settings detected, creating...")
        url = input("Enter webhook URL:\n")
        username = input("Enter your name:\n")
        with open("f3cender.json", "w") as jsonFile:
            json.dump({"url": url, "username": username}, jsonFile, indent=4)
            jsonFile.close()
    with open("f3cender.json", "r") as jsonFile:
        jsonDict = json.load(jsonFile)
        jsonFile.close()
    f3cender = F3Cender(jsonDict["url"], jsonDict["username"])
    f3cender.start()
    while input() != "stop":
        pass
    f3cender.stop()
