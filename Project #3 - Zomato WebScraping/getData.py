from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import pickle
import pandas as pd

class Review:
    def __init__(self) -> None:
        self.userLink = None
        self.restrauntName = None
        self.dishes = None
        self.stars = None
        self.text = None
        self.helpfulVites = None
        self.comments = None
        self.date = None
        self.type = None

    def print(self):
        print("user id: ", self.userLink)
        print("stars:" , self.stars)
        print("text:", self.text)
        print("type:", self.type)
        print("date:", self.date)
        print('\n')

    def isSame(self, review):
        if self.userLink == review.userLink and self.stars == review.stars and self.text == review.text and self.date == review.date:
            return True
        else:
            return False

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


if __name__ == "__main__":
    #getting restaurant list - like zomato.com + (restraunt list) thing gives the link. e.g) /ncr/dargeeling-momo-simethingtomsething
    with open('links4.pkl', 'rb') as f:
        restrauntList = pickle.load(f)
    print (restrauntList)

    counter = 0
    #iterate through restaurants
    for restraunt in restrauntList[0:]:
        reviews = []
        # get source code
        # browser.get("https://www.zomato.com/ncr/biryani-blues-sikandarpur/reviews")
        limit= 1000000000000
        j = 1
        while j < limit:
            #simualte chrome browser
            browser = webdriver.Chrome('./chromedriver')
            #+str(j) is cuz many reviews so have to go through 10000000000 (all) reviews. Last part is only use delivery not eat in
            linkRestraunt = "https://www.zomato.com" + restraunt + "reviews?page=" + str(j) + "&sort=dd&filter=reviews-dd"
            #enter link on browser
            browser.get(linkRestraunt)
            #Get html from browser. All html comes here in variable html
            html = browser.page_source
            #wait 2 seconds then close browser
            time.sleep(0.2)
            # close web browser
            browser.close()

            #html is a very big file. Has many divisions so need to find the div containing comments

            #Find correct division which contains the review. Once you find correct div then can extract reviews
            soup = bs(html, 'lxml')
            #soup gives arrow to open close but normally will get text. soup implements arrow type things
            body = soup.find('body')
            root = body.find('div', id='root')
            root2 = root.find('div')
            main = root2.find('main')
            mainDiv = main.find('div')
            section = mainDiv.contents[4]
            #first page is differet
            if j == 1:
                actualRatingpart = mainDiv.contents[2]
                s = actualRatingpart.find('section')
                s = s.find('section')
                d = s.find('div')
                d = d.find('div')
                d = d.find('div')
                s = d.find('section')

                dd = s.contents[2]
                d = s.find('div')

                dd = dd.find('div')
                dd = dd.find('div')
                dd = dd.find('div')
                deliveryRating = dd.find('div').text
                print(deliveryRating, 'delivery')

                d = d.find('div')
                d = d.find('div')
                d = d.find('div')
                diningRating = d.find('div').text
                print(diningRating, 'dining')

            div = section.find('div')
            div = div.find('div')
            section = div.contents[1]
            div = section.contents[2]


            numberifRevies = section.contents[1]
            ddd = numberifRevies.find('div')
            ddd = ddd.find('div')
            ddd = ddd.find('div')
            ddd = ddd.find('div')
            ddd = ddd.find('div')
            span = ddd.find('span')
            #div is the final div you found
            limit = int((int(find_between(span.find('p').text, '(', ')')))/5) + 2
            # print(div.prettify())

            #finds the section of the review based on the size
            def isUserdetailsSection(html):
                return 'height="4.4rem" width="4.4rem"' in html.prettify()

            def isStarsDiv(html):
                return 'height="2rem" width="2.6rem"' in html.prettify()

            def isHelpfulandCommentsSection(html):
                return 'Votes for helpful' in html.prettify()

            def isCommentEndsection(html):
                return 'width="16"' in html.prettify() 

            def isDishesSection(html):
                return 'size="12"' in html.prettify() 

            def isReviewText(html):
                global div
                return html in div.find_all('p')

            # i = 0
            # for c in div.contents:
            #     i += 1
            #     print(i)
            #     print(isUserdetailsSection(c), "users")
            #     print(isStarsDiv(c), "stars")
            #     print(isReviewText(c), "text")
            #     print(isHelpfulandCommentsSection(c), "helpful")
            #     print(isCommentEndsection(c), "end")
            #     print('\n')

            #stores data about each review using class Review
            i = 0
            while i < len(div.contents):
                c = div.contents[i]
                #gets link
                if isUserdetailsSection(c):
                    # New reveiew is starting
                    review = Review()
                    link = c.find('a', href=True)
                    # print(link['href'])
                    review.userLink = link['href']
                #gets stars (see the color of star and then on thebasis of that you can see the stars)
                if isStarsDiv(c):
                    # Get the stars that the review got
                    div_ = c.contents[0]
                    p = c.contents[1]
                    input_tag = div_.find(attrs={"color": "#24963F"}) # 4 stars
                    if not input_tag is None:
                        output = input_tag['color']
                        # print(output, '4')
                        review.stars = 4
                    input_tag = div_.find(attrs={"color": "#0E5020"})# 5 stars
                    if not input_tag is None:
                        output = input_tag['color']
                        # print(output, '5')
                        review.stars = 5
                    input_tag = div_.find(attrs={"color": "#EF4F5F"})# 1 stars
                    if not input_tag is None:
                        output = input_tag['color']
                        # print(output, '1')
                        review.stars = 1
                    input_tag = div_.find(attrs={"color": "#FF7E8B"})# 2 stars
                    if not input_tag is None:
                        output = input_tag['color']
                        # print(output, '2')
                        review.stars = 2
                    input_tag = div_.find(attrs={"color": "#E9B501"})# 3 stars
                    if not input_tag is None:
                        output = input_tag['color']
                        # print(output, '3')
                        review.stars = 3
                    div__ = div_.contents[1]
                    type_ = div__.text
                    review.type = type_
                    review.date = c.contents[1].text
                    # print(type_, "jbbhjkmbhkjbhj")
                #extract text
                if isReviewText(c):
                    review.text = c.text
                    # print(c.text)
                #if comment ends go on next page
                if isCommentEndsection(c):
                    go = True
                    for r in reviews[-6:]:
                        if r.isSame(review):
                            go = False
                    if go:
                        reviews.append(review)
                    review = Review()
                    #revew variable is like according to the class so review.rating gives rating.
                    # append review to list reviews, now then add +1 to i and do next review
                i += 1
                # print(i)

            #limit is basically not 1000000 so dont have to do this 1000000 times and only do it the number of reviews ka times
            print(j, limit, len(restrauntList))
            j += 1

        for r in reviews:
            r.print()

        print(len(reviews))
        #array of arrays, [khan chacha, 100 reviews (detailed variable so can do .stars, etc.), delivery rating on zomato, dining rating on zomato]
        pickle.dump([restraunt, reviews, deliveryRating, diningRating] , open(str(counter) + ".pkl", "wb"))
        #name of file is "counter"
        counter += 1
        # now need to get it in sets of five