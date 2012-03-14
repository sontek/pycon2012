$(document).ready(function() {
    // connect to the websocket
    socket = io.connect();
    chat = io.connect('/chat');

    // Listen for the event "chat" and add the content to the log
    socket.on("chat", function(e) {
        console.log("Chat message event", arguments);
        $("#chatlog").append(e + "<br />");
    });
    socket.on("message", function(e) {
        console.log("Message", e);
    });
    chat.on("pack", function(e) {
        console.log("got pack message", e);
    });
    socket.on("connect", function(e) {
        console.log("Connected", arguments);
    });
    chat.on("error", function(e) {
        console.log("Error", arguments);        
    });
    socket.on("disconnect", function(e) {
        console.log("Disconnected", arguments);
    });


    // Execute whenever the form is submitted
    $("#chat_form").submit(function(e) {
        // don't allow the form to submit
        e.preventDefault();

        var val = $("#chatbox").val();

        // send out the "chat" event with the textbox as the only argument
        socket.emit("chat", val);

        $("#chatlog").append(val + "<br />");

        $("#chatbox").val("");
    });

    $('#b1').click(function(){
        console.log("b1, emit bob, thank you")
        socket.emit("bob", {"thank": "you"});
    });
    $('#b2').click(function(){
        console.log("b2, send simple json message")
        socket.json.send({blah: "a simple message"});
    });
    $('#b3').click(function(){
        console.log("b3, json.emit(bob, {thank:you})")
        socket.json.emit("bob", {"thank": "you"});
        socket.send("a simple message");
    });
    $('#b4').click(function(){
        console.log("b4, send /chat elements")
        chat.emit('mymessage', 'bob');
        chat.send("hey");
        chat.json.send({asdfblah: "asd " + String.fromCharCode(13) + "fé\n\\'blah"});
    });
});
