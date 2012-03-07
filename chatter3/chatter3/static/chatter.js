$(document).ready(function() {
    // connect to the websocket
    var socket = io.connect();

    var ChatModel = Backbone.Model.extend({
    });

    var ChatItem = Backbone.View.extend({
        render: function(){
            var template = Handlebars.compile($("#chat_item_template").html());
            this.$el.html(template(this.model.toJSON()));

            return this;
        },
    });

    var ChatView = Backbone.View.extend({
        events: {
            "submit #chat_form": "send"
        },

        send: function(evt) {
            evt.preventDefault();
            var val = $("#chatbox").val();

            socket.emit("chat", val);
            $("#chatbox").val("");
        },

        initialize: function() {
            var me = this;

            socket.on("chat", function(e) {
                me.$("#chatlog").append(new ChatItem({
                    model: new ChatModel({
                        chat_line: e
                    })
                }).render().el);
            });
        },

        render: function(){
            var template = Handlebars.compile($("#chat_template").html());
            $(this.el).html(template());
        },

    });

    var Router = Backbone.Router.extend({

        routes: {
            "": "index"
        },

        index: function() {
            var view = new ChatView({
                el: $("#container"),
            });

            view.render();
        }

    });

    var router = new Router();
    Backbone.history.start({ pushState: true });

});
