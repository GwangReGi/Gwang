from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime;
import csv;
import time
import urllib.request

# --------make chrome driver-------------------------

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(chrome_options=chrome_options);

t = ['월', '화', '수', '목', '금', '토', '일']


# ----------------------------------

# 0 : get Date
# 1 : get Time
def getToday(n):
    now = datetime.datetime.now()

    if (n == 0):
        now = str(now.strftime('%Y-%m-%d'))
    elif (n == 1):
        now = str(now.strftime('%H:%M:%S'))
    elif (n == 2):
        now = t[datetime.datetime.today().weekday()]
    return now


def getInfo_id(page):
    url = "http://www.10000recipe.com/recipe/list.html?order=date&page=" + str(page)
    print(url)

    driver.get(url)

    time.sleep(10)

    lists = driver.find_elements_by_xpath("//div[@id = 'contents_area']//div[@class = 'col-xs-4']")

    output_imagepath = "/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/그림/"

    for list in lists:

        try:
            src = list.find_element_by_tag_name("a").get_attribute("href")
            src = str(src)
            id = str(src)[len(src) - 7: len(src)]

            img_url = list.find_element_by_tag_name("a").find_elements_by_tag_name("img")
            img_url = img_url[len(img_url) - 1].get_attribute("src")
            # img = list.find_element_by_class_name("thumbnail_over").find_element_by_tag_name("img").get_attribute("src")
            print(img_url)

            img_name = getToday(0) + "_" + id
            img_path = output_imagepath + img_name + ".jpg"
            urllib.request.urlretrieve(img_url, img_path)

            title = list.find_element_by_class_name("caption").find_element_by_tag_name("h4").text
            cooker = list.find_element_by_class_name("caption").find_element_by_tag_name("p").text
            cooker = str(cooker).replace("by ", "")

            writer.writerow([id, title, cooker, str(img_url)])

        except AttributeError as e:
            print(e)


def getInfo_recipe_range(startId, endId):
    filepath = "/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/Text/text_recipe10000_" + str(startId) + "_" + str(endId)

    fw = open(filepath, 'w', encoding='utf-8')
    global writer_recipe
    writer_recipe = csv.writer(fw)
    writer_recipe.writerow(["Id", "view_num", "cooker", "summary", "ingredient", "tag", "notice", "rec_recipe" , "rec_tag" , "step"])

    for i in range(startId, endId):
        getInfo_recipe(i)


def getInfo_recipe(id):

    try:
        url = "http://www.10000recipe.com/recipe/" + str(id)
        print(url)

        driver.get(url)

        time.sleep(10)

        result = []

        result.append(str(id))

        try:
            lists = driver.find_element_by_id("contents_area")
        except:
            print("cannot find page")

        try:
            picture = lists.find_element_by_class_name("view2_pic")
            view_num = picture.find_element_by_class_name("view_cate_num")
            result.append(view_num.text)
            cooker = picture.find_element_by_class_name("user_info2")
            result.append(cooker.text)
        except:
            result.append("no_data")
            result.append("no_data")


        try:
            summary = lists.find_element_by_class_name("view2_summary")
            result.append(summary.text)
        except:
            result.append("no_data")

        try:
            ingredient = lists.find_element_by_id("divConfirmedMaterialArea")
            result.append(ingredient.text)
        except:
            try:
                ingredient = lists.find_element_by_id("divConfirmedMaterialArea")
                result.append(ingredient.text)
            except:
                result.append("no_data")


        try:
            step_container = lists.find_element_by_class_name("view_step")

            tag = step_container.find_element_by_class_name("view_tag")
            notice = step_container.find_element_by_class_name("view_notice").find_element_by_tag_name("p")
            result.append(tag.text)
            result.append(notice.text)
        except:
            result.append("no_data")
            result.append("no_data")

        try:
            recommend_recipes = lists.find_element_by_class_name("view_pdt_recipe").find_elements_by_tag_name("a")
            reco_recipe = "";
            for recommend_recipe in recommend_recipes:
                temp = str(recommend_recipe.get_attribute("href"))
                id = str(temp)[len(temp) - 7: len(temp)]

                reco_recipe = reco_recipe + "-" + id

            result.append(reco_recipe)
        except:
            result.append("no_data")

        try:
            recommend_tags = lists.find_element_by_class_name("view_pdt_recipe2").find_elements_by_tag_name("li")
            reco_tag = "";

            for recommend_tag in recommend_tags:
                temp = str(recommend_tag.find_elements_by_tag_name("a")[1].get_attribute("href"))
                id = str(temp)[len(temp) - 7: len(temp)]
                reco_tag = reco_tag + "-" + id

            result.append(reco_tag)
        except:
            result.append("no_data")

        try:

            steplists = step_container.find_elements_by_class_name("view_step_cont")

            for step in steplists:
                result.append(step.text)

        except:
            result.append("no_data")

        try:
            oldText = lists.find_element_by_id("oldContArea")
            result.append(oldText.text)
        except:
            print("cannot find old Text")

        writer_recipe.writerow(result)


    except:
        writer_recipe.writerow(id , "error")
        print("error in find recipe")

# print(result)


def getInfo_id_range(startPage, endPage):
    filepath = "/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/id/recipe10000_" + str(startPage) + "_" + str(endPage)

    fw = open(filepath, 'w', encoding='utf-8')
    global writer
    writer = csv.writer(fw)

    for i in range(startPage, endPage):
        getInfo_id(i)


#for i in range(19, 30):
#   getInfo_id_range(i*100, (i+1)* 100)

#for i in range(1 , 10):
#    getInfo_recipe_range((6880828 - i*100) , (6880828 - (i-1)*100) )

getInfo_recipe_range( 6880550 , 6880650 )
