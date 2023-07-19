from googlesearch import search #pip install googlesearch-python
from bs4 import BeautifulSoup #pip install bs4
import requests #pip install requests
from googletrans import Translator #pip install googletrans==4.0.0-rc1

def search_question(query): #function search
    a = ""  # Khởi tạo biến 'a'
    try:
        search_results = search(query, num_results=5, lang='vi') #query là câu hỏi , num_results là số lượng câu hỏi tìm kiếm ( đừng để cao quá nó search lâu lắm =)) ) , lang  là ngôn ngữ nhập

        for result in search_results:
            #chạy for để check cái search kia (
         # để dễ hiểu hơn thì lua thì nó là table ví dụ local a  = {1,2,3} thì để xem số 1 2 3 thì mấy ông cần 
            #for i,v in pairs(a) do  
            # print(v) -> 1,2,3
            # end
            #<=> python cung nhu the nha =))
            #( result lúc này là link web )
            response = requests.get(result) #xài requests để lấy data từ result
            soup = BeautifulSoup(response.text, 'html.parser') # cái này không biết tại check var =))
            answer = soup.find('div', class_='mw-parser-output') #tìm mấy cái thẻ <div> trong html còn class là cái gì thì tui d bt
            a = result # call a = result 
            if answer: # nếu answer d phải là 0 hay nil
                return answer.get_text(),a  # Trả về cả giá trị của 'answer' và 'a'

    except Exception as e:
        print("Đã xảy ra lỗi:", str(e)) # check lỗi thôi

    return "Không tìm thấy câu trả lời."  # trả về giá trị nếu k thì thấy câu trả lời
# tui dùng google dịch vì không dịch thì cái anser.get_text() nó k work nhé hihi
def translate_text(text, dest_lang='vi', translate=True): #translate câu trả lời ( đặt nó có giá trị true vì nếu dài quá api d dịch đc đâu nên phải sút thành false)
    translator = Translator(service_urls=['translate.google.com'])
    if translate:
        translated_text = translator.translate(text, dest_lang)
        return translated_text.text
    else:
        return text


def translate_text2(text, dest_lang='en'): #dịch câu hỏi sang tiếng anh để answer.get_text() hoạt động
    translator = Translator(service_urls=['translate.google.com'])
    translated_text = translator.translate(text, dest_lang)
    return translated_text.text

def main():
    while True: #lập lại đến chết
        question = input("Nhập câu hỏi của bạn (hoặc bấm Ctrl + c để thoát): ") #input câu hỏi
        translate_question = translate_text2(question) # dịch câu hỏi sang tiếng anh
        answer, a = search_question(translate_question)  
        # lấy giá trị answer và a khi search cái vừa dịch phía trên ( a là link web nha hihi)
        
        if 'wikipedia' in a: # check nếu nó là wiki
            translated_answer = translate_text(answer, translate=False) #d dịch do nó dài quá api bị ngu 
        else:
            translated_answer = translate_text(answer) #dịch
        if answer == "": #check nếu câu trả lời return là nil
            print("Câu Trả lời dài quá nên không dịch được, tham khảo tạm ở: \n"+a)
        else:
            print("Câu trả lời: ", translated_answer)
            print("Câu trả lời có thể bị ngu bạn có thể tham khảo ở: \n" + a)
            #note: Cái này nó dễ bị ngu lắm có gì thông cảm

if __name__ == "__main__":
    main()
