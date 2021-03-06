from lxml import html
import requests
import json

class Quest:
    def __init__(self, quest_name,quest_points, quest_length, member_required,quest_url,requirements,id):
        self.name = str.rstrip(quest_name)
        self.quest_points_reward = str.rstrip(quest_points)
        self.length = str.rstrip(quest_length)
        self.membership_requirement = member_required
        self.url = 'http://oldschoolrunescape.wikia.com' + quest_url
        self.requirements = str(requirements)
        self.id = id

    def to_dict (self):
        return {"name": self.name, "quest_points_reward": self.quest_points_reward, "length": self.length,"membership_requirement": self.membership_requirement,"url": self.url,"requirements": self.requirements}

def scrape():
    print("Scraping runescape wiki for latest quest details (might take a while)...")
    page = requests.get('http://oldschoolrunescape.wikia.com/wiki/Quest_info_table')
    tree = html.fromstring(page.content)

    quests_name = tree.xpath('//*[@id="mw-content-text"]/table/tr[*]/td[1]/a/text()')
    quests_points = tree.xpath('//*[@id="mw-content-text"]/table/tr[*]/td[2]/text()')
    quests_length = tree.xpath('//*[@id="mw-content-text"]/table/tr[*]/td[3]/text()')
    quests_membership_requirement = tree.xpath('//*[@id="mw-content-text"]/table/tr[*]/td[4]/a/@title')
    quests_url = tree.xpath('//*[@id="mw-content-text"]/table/tr[*]/td[1]/a/@href')

    for i in range(0,len(quests_membership_requirement)):
        if quests_membership_requirement[i] == "This content is available to all players.":
            quests_membership_requirement[i] = False
        else:
            quests_membership_requirement[i] = True

    quests_list = []

    # Create quest objects
    for i in range(0,len(quests_name)):
        # Also grab the list of requirements
        quest_requirements = html.fromstring(requests.get("http://oldschoolrunescape.wikia.com" + quests_url[i]).content).xpath('''
            //*[@id="mw-content-text"]/table[2]/tr[5]/text()
            |//*[@id="mw-content-text"]/table[2]/tr[5]/td[2]/text()
            |//*[@id="mw-content-text"]/table[2]/tr[5]/td[2]/node()/text()
            |//*[@id="mw-content-text"]/table[2]/tr[5]/td[2]/node()/node()/text()
            |//*[@id="mw-content-text"]/table[2]/tr[5]/td[2]/node()/node()/node()/text()
            |//*[@id="mw-content-text"]/table[2]/tr[5]/td[2]/node()/node()/node()/node()/text()
            |//*[@id="mw-content-text"]/table[2]/tr[5]/td[2]/node()/node()/node()/node()/node()/text()
            |//*[@id="mw-content-text"]/table[2]/tr[5]/td[2]/node()/node()/node()/node()/node()/node()/text()
            |//*[@id="mw-content-text"]/table[2]/tr[5]/td[2]/node()/node()/node()/node()/node()/node()/node()/text()
            |//*[@id="mw-content-text"]/table[3]/tr[5]/text()
            |//*[@id="mw-content-text"]/table[3]/tr[5]/td[2]/text()
            |//*[@id="mw-content-text"]/table[3]/tr[5]/td[2]/node()/text()
            |//*[@id="mw-content-text"]/table[3]/tr[5]/td[2]/node()/node()/text()
            |//*[@id="mw-content-text"]/table[3]/tr[5]/td[2]/node()/node()/node()/text()
            |//*[@id="mw-content-text"]/table[3]/tr[5]/td[2]/node()/node()/node()/node()/text()
            |//*[@id="mw-content-text"]/table[3]/tr[5]/td[2]/node()/node()/node()/node()/node()/text()
            |//*[@id="mw-content-text"]/table[3]/tr[5]/td[2]/node()/node()/node()/node()/node()/node()/text()
            |//*[@id="mw-content-text"]/table[3]/tr[5]/td[2]/node()/node()/node()/node()/node()/node()/node()/text()
            ''')

        quest = Quest(quests_name[i],quests_points[i], quests_length[i], quests_membership_requirement[i],quests_url[i],''.join(quest_requirements),i)
        quests_list.append(quest)

    results = [obj.to_dict() for obj in quests_list]

    with open('quests.json', 'w') as outfile:
        json.dump(results,outfile)
        
    print("\nDone!")

if __name__ == '__main__':
    scrape()

