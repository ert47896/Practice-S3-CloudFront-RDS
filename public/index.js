// Models
let models = {
    // API回復資料
    data:null,
    // API回復狀態碼
    responseStatus:0,
    // 向API索取資料
    getData:function(url){
        return fetch(url).then((response)=>{
            this.responseStatus = response.status;
            return response.json();
        }).then((result)=>{
            this.data = result.data;
        });
    }
};
// Views
let views = {
    renderData:function(data){
        const mainContainer = document.querySelector("main");
        mainContainer.innerHTML = "";
        for(i=0;i<data.length;i++){
            const messageContainer = document.createElement("section");
            const textElement = document.createElement("p");
            const imgElement = document.createElement("img");
            const hrElement = document.createElement("hr");
            textElement.textContent = data[i].message;
            imgElement.src = data[i].file_url;
            imgElement.alt = "photo";
            messageContainer.appendChild(textElement);
            messageContainer.appendChild(imgElement);
            messageContainer.appendChild(hrElement);
            mainContainer.appendChild(messageContainer);
        };
    }
}
// Controllers
let controllers = {
    // 初始化
    init:function(){
        const apiUrl = window.location.origin + "/api/message";     //window.location.origin 伺服器主機網址
        // 向API要message資料
        models.getData(apiUrl).then(()=>{
            views.renderData(models.data);
        });
    }
}
controllers.init();