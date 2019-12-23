function AJAX_get_price(data) {

    function collect_data_for_price_prediction(features_list){
        let data_for_price_prediction = [];
        for(let index = 0; index < features_list.length; index++){
            data_for_price_prediction.push(features_list[index] + "=" + document.getElementById(features_list[index]).value)
        }
        return data_for_price_prediction
    }

    let features = [];
    for(let i = 0; i < data.length; i++) {
        features.push(data[i]["feature"])
    }
    let features_data = collect_data_for_price_prediction(features).join("&");
    console.log(features_data);

    $.ajax({
        type: "GET",   // Тип запроса
        url: "/get_price",   // Путь к сценарию, обработающему запрос
        dataType: "json",   // Тип данных, в которых сервер должен прислать ответ
        data: features_data,
        error: function () {
            console.log("При выполнении запроса произошла ошибка :(");
        },
        success: function (response) {
            let data = "";
            if (response["error"] === 1){
                data = response["error_text"]
            }
            else {
                data = "Стоимость квартиры указанного типа составит примерно: " + response["price"] + " рублей"
            }

            document.getElementById("price_form").style.visibility = "visible";
            document.getElementById("price_form").innerText = data;
        }
    })
}
