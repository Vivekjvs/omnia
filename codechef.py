
url = "https://www.codechef.com/users/vivekjvs"
page = requests.get(url)

soup = BeautifulSoup(page.content,"html5lib")
val = soup.find_all("script")[39].text
index = val.index("all_rating") + 13
string = ""
while val[index] != ";":
    string += val[index]
    index += 1
print (int(json.loads(string)[-1]['rating']))