var app = {

    views: {},

    models: {},

    loadTemplates: function(views, callback) {

        var deferreds = [];

        $.each(views, function(index, view) {
            if (app[view]) {
                deferreds.push($.get('static/tpl/' + view + '.html', function(data) {
                    app[view].prototype.template = _.template(data);
                }, 'html'));
            } else {
                alert(view + " not found");
            }
        });

        $.when.apply(null, deferreds).done(callback);
    }

};

app.Router = Backbone.Router.extend({

    routes: {
    },

    initialize: function () {
     this.$content = $("#content"); 
     this.login();
    },

    home: function () {
        // Since the home view never changes, we instantiate it and render it only once
        if (!app.homelView) {
            app.homelView = new app.HomeView();
            app.homelView.render(null);
        } else {
            console.log('reusing home view');
            app.homelView.delegateEvents(); // delegate events when the view is recycled
        }
        this.$content.html(app.homelView.el);
    },

    login: function() {
        if (!app.loginView) {
            app.loginView = new app.LoginView();
            app.loginView.render(null);
        } else {
            console.log("reusing login view");
            app.loginView.delegateEvents();
        }
        this.$content.html(app.loginView.el);
    }

});

$(document).on("ready", function () {
    app.loadTemplates(["HomeView", "LoginView"],
        function () {
            app.router = new app.Router();
            Backbone.history.start();
        });
});
