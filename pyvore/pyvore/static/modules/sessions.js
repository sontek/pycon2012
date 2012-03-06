(function(Sessions) {
    Sessions.Views.SessionList = Pyvore.View.extend({
        template: "session_list"
    });

    Sessions.Models.Chat = Backbone.Model.extend({
    });

    Sessions.Views.Chat = Pyvore.View.extend({
        events: {
            "click #send": "send"
        },

        template: "chat",

        initialize: function() {
            var me = this;
            Pyvore.View.prototype.initialize.call(this);

            Pyvore.socket.on("chat", function (e) {
                me.collection.add(new Sessions.Models.Chat({
                    body: e
                }));
            });
        },

        send: function() {
            var val = this.$("#txtChat").val();
            var id = this.collection.pk;
            Pyvore.socket.emit("chat", this.collection.pk, val);
            this.$("#txtChat").val("");
        }
    });

    Sessions.Collections.Chat = Backbone.Collection.extend({
        initialize: function(models, pk) {
            var me = this;
            this.pk = pk;
        },

        url: function () {
            return '/api/sessions/' + this.pk
        }
    });

    Sessions.Collections.SessionCollection = Backbone.Collection.extend({
        url: '/api/sessions/'
    });

})(Pyvore.module("sessions"));
