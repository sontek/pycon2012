$(document).ready(function() {
    // connect to the websocket
    var socket = io.connect();

    socket.on("chat", function(e) {
        $("#chatlog").append(e + "<br />");
    });

    // Execute whenever the form is submitted
    $("#chat_form").submit(function(e) {
        // don't allow the form to submit
        e.preventDefault();

        var val = $("#chatbox").val();

        socket.emit("chat", val);
        $("#chatbox").val("");
    });
});
