var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var big5socket = new WebSocket(ws_scheme + '://' + window.location.host + "/bigfive/{{participant.code}}");

var old_answers;
var anss;
var i = 0;
var participant_code = "{{ participant.code }}";

$('input[name^="survey"]').on('click', function () {
    arr_to_send = {};
    $('input[name^="survey"]:checked').each(function (index, value) {
        arr_to_send[value.name.substring(8)] = value.value;
    });
    send_answers(arr_to_send);
});


send_answers = function (answers) {
    var msg = {
        participant_code: participant_code,
        answers: answers
    };
    if (surveysocket.readyState === surveysocket.OPEN) {
        surveysocket.send(JSON.stringify(msg));
    }
};


window.onload = function () {
    i = 0;
    old_answers = {{old_data |safe}};
    console.log(old_answers);
    ;
    for (var ans = 0; ans < {{num_questions }}
    ;ans++
)
    {
        anss = old_answers[ans] - 1;
        if (anss > -1) {
            $("input#id_survey_" + i + "_" + anss).prop("checked", true);
        }
        i += 1;
    }
};



