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
        "": "home",
        "login": "login",
        "register": "register",
    },

    initialize: function () {
        app.shellView = new app.ShellView();
        $('body').html(app.shellView.render().el);
        // Close the search dropdown on click anywhere in the UI
        $('body').click(function () {
            $('.dropdown').removeClass("open");
        });
        this.$content = $("#content"); 
        this.register();
    },

    home: function() {
        // Since the home view never changes, we instantiate it and render it only once
        if (!app.homeView) {
            app.homeView = new app.HomeView();
            app.homeView.render(null);
        } else {
            console.log('reusing home view');
            app.homeView.delegateEvents(); // delegate events when the view is recycled
        }
        this.$content.html(app.homeView.el);
        app.homeView.selectMenuItem('home-menu');
    },
    register: function () {
        // Since the home view never changes, we instantiate it and render it only once
        if (!app.registerView) {
            app.registerView = new app.RegisterView();
            app.registerView.render(null);
        } else {
            console.log('reusing register view');
            app.registerView.delegateEvents(); // delegate events when the view is recycled
        }
        this.$content.html(app.registerView.el);
        app.shellView.selectMenuItem('register-menu');
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
        app.shellView.selectMenuItem('login-menu');
    }

});

$(document).on("ready", function () {
    app.loadTemplates(["ShellView", "RegisterView", "LoginView", "HomeView"],
        function () {
            app.router = new app.Router();
            Backbone.history.start();
        });
});
