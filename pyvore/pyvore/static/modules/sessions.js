(function(Sessions) {
    Sessions.Views.SessionList = Pyvore.View.extend({
        template: "session_list"
    });

    Sessions.Models.Chat = Backbone.Model.extend({
    });

    Sessions.Views.Chat = Pyvore.View.extend({
        events: {
            "click #send": "send",
            "keydown #txtChat": "check_send"
        },

        template: "chat",

        render: function(manage) {
            return manage(this).render().then(function(el) {
                console.log("AFTER RENDER!");
                $(el).find("#txtChat").each(function(txt) {
                    $(txt).focus(); 
                });
            });
        },

        serialize: function() {
            var me = this;

            context = Pyvore.View.prototype.serialize.call(this);

            var session = '';

            for(var i=0; i < Pyvore.sessions.models.length; i++) {
                if (Pyvore.sessions.models[i].id == me.collection.pk) {
                    session = Pyvore.sessions.models[i];
                }
            }

            if (session != '') {
                context['session'] = session.toJSON();
            }

            return context;
        },

        initialize: function() {
            var me = this;

            Pyvore.View.prototype.initialize.call(this);

            Pyvore.socket.on("chat", function (data) {
                me.collection.add(data)
            });
        },

        check_send: function(event) {
            if (event.keyCode == 13) {
                this.send();
            }
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
