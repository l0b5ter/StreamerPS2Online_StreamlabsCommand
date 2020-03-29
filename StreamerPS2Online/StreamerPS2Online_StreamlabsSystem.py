#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
sys.platform = "win32"
import os, threading, json, codecs, traceback, time
import re
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "StreamerPS2Online"
Website = "https://github.com/l0b5ter/StreamerPS2Online_StreamlabsCommand"
Description = "Chat can now control your keyboard!"
Creator = "lobster/loster31345"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------

global Factions
global baseapi 
global Playername
baseapi = "https://census.daybreakgames.com/s:lobster/get/ps2:v2/"
Factions = ["nc", "tr", "vs"]

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global CommandFileList
    directory = os.path.join(os.path.dirname(__file__), "Config")
    if not os.path.exists(directory):
        os.makedirs(directory)
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == "stats": 
        for x in Factions:
            OnlineWho = PlayerLoopUp(x)
            if OnlineWho != "":
                SendResp(data, "Online " + OnlineWho)
                return
    return

def PlayerLoopUp(faction):
    status = ""
    CommandFile = os.path.join(os.path.dirname(__file__), 'Config/' + faction + '.json')
    CommandFileList = MySettings(CommandFile)
    OnlinePlayer = re.findall(r"[\w']+", CommandFileList.player)
    for i in OnlinePlayer:
        Playername = i.lower()
        Parent.Log(ScriptName, Playername)
        if GetOnlinePlayer(i) == "true":
            status = i
            return  status
    return status


def GetOnlinePlayer(playerlist):
    IsOnline = ""
    
    api = baseapi + "character/?name.first_lower=" + playerlist.lower() +"&c:join=characters_online_status&c:limit=5000"
    #Parent.SendStreamMessage(api)
    apidata = json.loads(Parent.GetRequest(api, {}))
    apiresponse = json.loads(apidata['response'])
    #Parent.Log(ScriptName, json.dumps(apiresponse))
    #Parent.Log(ScriptName, api)
    for character in apiresponse["character_list"]:
        Parent.Log(ScriptName, str(character["character_id_join_characters_online_status"]))
        if character["character_id_join_characters_online_status"]["online_status"] != "0":
            IsOnline = "true"
        else:
            IsOnline = "false"
    return IsOnline

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return


#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return



def SendResp(data, Message):

    if not data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendStreamMessage(Message)

    if not data.IsFromDiscord() and data.IsWhisper():
        Parent.SendStreamWhisper(data.User, Message)

    if data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendDiscordMessage(Message)

    if data.IsFromDiscord() and data.IsWhisper():
        Parent.SendDiscordDM(data.User, Message)
    return
