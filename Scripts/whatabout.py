import wikipedia
import sys

from wikipedia.exceptions import DisambiguationError, PageError
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from colorama import init

init()

arguments = []
for arg in sys.argv[1:]:
    arguments.append(arg)

if "$" in arguments[0]:
    query = arguments[0].replace("$"," ")
else:
    query = arguments[0]

print(Fore.GREEN + "\n \n Searching info for " + Fore.CYAN + f"{query} \n")

def wikipage(st):
    try:
        consult  = wikipedia.page(st.lower()).html()
        try:
            summary  = wikipedia.summary(st.lower())
        except:
            summary  = " +++ "
        return [consult, summary, st];
    except DisambiguationError:
        disambiguation  = wikipedia.page(st.lower(),sm=True)
        pages = disambiguation.refs
        print(Fore.GREEN)
        print(f"It seems that there are a disambiguation for {st} \n")
        print("Please try choosing one of the following options: \n")
        print(Fore.CYAN)
        for i in range(len(pages)):
            print(Fore.BLUE+str(i) + "-.    " +Fore.CYAN +pages[i])
        ans = input(Fore.LIGHTMAGENTA_EX + " Option : " + Fore.CYAN + "")
        return wikipage(pages[int(ans)]);
    except PageError:
        print("\n")
        print(Fore.LIGHTMAGENTA_EX + f"Oops! It seems that there is no available info for {st}")
        print("\n")
        sys.exit()

page = wikipage(query)

print(Fore.CYAN + "\n" +"Currently seeing:  "+ Fore.LIGHTYELLOW_EX +f"{page[2]} \n")
print("\n" + Fore.GREEN+page[1]+"\n")

page_soup = BeautifulSoup(page[0], "lxml")
content_tab  = page_soup.find("div", attrs={"id":"toc", "class":"toc"})

rt = content_tab.findAll("span" ,attrs = {"class":"toctext"})
rn = content_tab.findAll("span" ,attrs = {"class":"tocnumber"})

conttab = {}

for i in range(0,len(rt)):
    conttab.update({rn[i].text:rt[i].text})
    ident = rn[i].text.count(".")
    print(Fore.BLUE + "\t"*ident + rn[i].text +" -"  + Fore.CYAN +" " + rt[i].text)

print("\n")

siblings = content_tab.find_next_siblings()
if siblings == []:
    for i in range(1,10):
        try:
            toc = "toclimit-"+str(i)
            siblings = page_soup.find("div", attrs={"class":toc}).find_next_siblings()
        except:
            pass

navigation = {}
content    = ["Results are showed in the subsections: \n"]
last_key   = None
for tag in siblings:
    if (tag.name in ["h2","h3","h4","h5","h6","h7","h8","h9"]):
        navigation.update({ tag.text.replace("[edit]",""):content })
        last_key = tag.text.replace("[edit]","")
        content = []
    elif (tag.name == "p"):
        content.append(tag.text)
        navigation.update({ last_key:content })
    else:
        pass
def show_section(number):
    number = str(number)
    pass_key = conttab.get(number)
    info = navigation.get(pass_key)
    print("\n Showing :  " + Fore.CYAN +pass_key + "\n")
    for item in info:
        print(Fore.GREEN+item)
    print("\n")
    return;

while True:
    section = input(Fore.LIGHTMAGENTA_EX + "\n Section to see (or press x to exit):   "+Style.RESET_ALL)
    if "x" in section:
        break
    else:
        show_section(section)

# with open("file.html", "w", encoding="utf-8") as f:
#     f.write(page)

