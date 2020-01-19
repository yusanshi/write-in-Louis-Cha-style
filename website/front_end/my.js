window.onload = initial;

$(function () {
    $('#submitForm').on('submit', function (e) {
        e.preventDefault();
        var begining = document.getElementById("begining").value;
        var length = document.getElementById("length").value;
        var temperature = document.getElementById("temperature").value;

        var lengthInt = parseInt(length);
        var temperatureFloat = parseFloat(temperature);
        if (begining.length == 0 || begining.length > 50) {
            alert("开头长度有误！（1 - 50）");
        } else if (isNaN(lengthInt) || lengthInt <= 0 || lengthInt > 2000) {
            alert("字数有误！（1 - 2000）");
        } else if (isNaN(temperatureFloat) || temperatureFloat <= 0 || temperatureFloat > 1) {
            alert("温度值有误！");
        } else {
            apply(begining, lengthInt, temperatureFloat);
        }
    });
});

async function initial() {
    model = await tf.loadLayersModel('https://yusanshi.com/Louis_Cha/tfjs/model.json');
    $.getJSON("data.json", function (data) {
        i2t = data.int_to_text;
        t2i = data.text_to_int;
    });
    updateText();
}

async function apply(begining, length, temperature) {
    document.getElementById("showArea").textContent = "正在生成中，请稍候……";

    $.ajax({
        url: "https://yusanshi.com/api/jieba",
        type: "POST",
        data: {
            "sentence": begining
        },
        dataType: "json",

        success: function (data) {

            var input_seq_int = [];
            for (const word of data) {
                if (word in t2i) {
                    input_seq_int.push(t2i[word]);
                }
            }

            if (input_seq_int.length == 0) {
                input_seq_int.push(t2i['<br>']);
            }
            var input_seq_int = tf.tensor(input_seq_int);
            var input_seq = input_seq_int.expandDims(0);

            var text_generated = '';
            model.resetStates();

            while (text_generated.length < length) {
                var predictions = model.predict(input_seq);
                var predictions = predictions.squeeze(0);
                var unstacked = predictions.unstack();
                var predictions = unstacked[unstacked.length - 1];
                var predictions = predictions.div(tf.scalar(temperature));
                var predictedID = tf.multinomial(predictions, 1).dataSync()[0];
                if (predictedID == 0) {
                    predictedID = t2i["<br>"];
                    console.log("Wrong at: " + text_generated.length);
                }
                var predictedIDList = [];
                predictedIDList.push(predictedID);
                var predictedIDTensor = tf.tensor(predictedIDList);
                var input_seq = predictedIDTensor.expandDims(0);
                text_generated += i2t[predictedID];
            }

            document.getElementById("showArea").innerHTML = begining + text_generated;
        },

        error: function () {
            document.getElementById("showArea").textContent = "获取分词信息失败！";
        }
    });
}

function updateText() {
    var x = document.getElementById("information");
    x.textContent = "模型加载完成！";
    x.setAttribute("class", "alert alert-success");
    document.getElementById("uniqueButton").removeAttribute("disabled");
}
