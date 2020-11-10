import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import csv
import logging

#課題７（ロガーを取得する）
logger = logging.getLogger(__name__)
format = "%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(message)s"
logging.basicConfig(filename='logger.log', level=logging.DEBUG,format=format)

### Chromeを起動する関数
def set_driver(driver_path,headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    #options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path,options=options)

### main処理
def main():
    data_count = 1
    df = pd.DataFrame(columns=['name','copy','status','job'])
    # 課題4（任意の項目で検索）
    input_keywored = input("検索のキーワードを入力してください：")
    search_keyword = input_keywored
    # driverを起動
    driver = set_driver("chromedriver",False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる（2個でてくるので２回実施）
    driver.execute_script('document.querySelector(".karte-close").click()')
    driver.execute_script('document.querySelector(".karte-close").click()')
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    # 課題3(次ページがなくなるまで繰り返し)
    while True:
        # 条件に合致した検索結果を全て取得
        # 課題6（データがなかった場合、空白で埋めて処理を続行するようにtry文を追加）
        try:
            name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        except:
                name_list = " "
        try:
             copy_list = driver.find_elements_by_class_name("cassetteRecruit__copy")
        except:
                copy_list = " "
        try:
             status_list = driver.find_elements_by_class_name("labelEmploymentStatus")
        except:
                status_list = " "
        try:
             job_list = driver.find_elements_by_class_name("tableCondition__body")
        except:
                job_list = " "
        # 課題２(1ページ分繰り返し)
        # print("{},{},{},{}".format(len(copy_list),len(status_list),len(name_list),len(job_list)))
        for name,copy,status,job in zip(name_list,copy_list,status_list,job_list):
            # 課題１（取得情報書き出し）
            logger.info(str(data_count) + '件目の出力を開始します')
            print(name.text)
            print(copy.text)
            print(status.text)
            print(job.text)
            # 一次元データ構造に取得データを格納（これをしないとappend上手く行かない...）
            df_add = pd.Series([name.text,copy.text,status.text,job.text], index=df.columns)
            # ignore=Trueにすることで縦連結に対応
            df = df.append(df_add, ignore_index = True)
            data_count += 1

        # 次のページボタンがあればクリックなければ終了
        ## 課題３
        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
        # 最終ページでは,iconFont--arrowLeftには値が入らずlen = 0となる
        if len(next_page) >= 1:
            # iconFont--arrowLeftのhrefの情報を抽出
            next_page_link = next_page[0].get_attribute("href")
            driver.get(next_page_link)
        else:
            # 課題5（取得したデータをcsvで取得）
            df.to_csv("pandas_test.csv")
            print("最終ページです。終了します。")
            logger.info(str(data_count)+ '件出力しました' )
            break

### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()  
