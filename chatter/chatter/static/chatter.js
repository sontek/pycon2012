$(document).ready(function() {
    // connect to the websocket
    var socket = io.connect();

    // Execute whenever the form is submitted
    $("#chat_form").submit(function(e) {
        // don't allow the form to submit
        e.preventDefault();

        var val = $("#chatbox").val();
        $("#chatlog").append(val + "<br />");
        $("#chatbox").val("");
    });
});
