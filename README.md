# [圖文留言板](https://board.taipeilife.info/)

本專案提供使用者圖文留言功能

## Demo
點擊網址前往圖文留言板網頁：https://board.taipeilife.info/

## 使用技術
* 以 Python Flask 框架建立網站
* 部署網頁於 AWS EC2
* 於 AWS RDS 建立資料庫
* 透由 boto3 連接 AWS S3 儲存圖片
* 透過 AWS CloudFront 建立 CDN 系統
* 透由 Let's Encrypt 申請 SSL 憑證實踐 HTTPS

## 系統架構圖
![image](https://user-images.githubusercontent.com/24973056/128723555-248d9386-98fa-4242-b41d-9841fb622563.png)

## 功能介紹
使用者輸入圖文內容點擊送出後，留言區即顯示所輸入內容

![image](https://user-images.githubusercontent.com/24973056/128659267-da0996a9-9bc6-465d-9ce4-667e9ed41dd8.png)

![image](https://user-images.githubusercontent.com/24973056/128659286-f9a4841b-ea2f-4908-a171-8f6ce212b163.png)
