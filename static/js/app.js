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
        "home": "home",
        "login": "login",
        "logout": "logout",
        "register": "register",
    },

    initialize: function () {
        app.credential = new app.Credential();
        app.credential.bind('change:loggedIn', this.landingPage, this);
        this.landingPage();
    },

    landingPage: function() {
        var loggedIn = app.credential.get('loggedIn');
        this.$content = $("#content");
        if (!loggedIn) {
          this.register();
        } else {
          this.shell();
        }
    },

    shell: function() {
      if (!app.shellView) {
        app.shellView = new app.ShellView();
      } else {
         console.log('reusing shell view');
         app.shellView.delegateEvents();
      } 
     $('body').html(app.shellView.render().el);
     $('body').click(function () {
            $('.dropdown').removeClass("open");
     });

     this.$content = $("#content");
     this.home();
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
    },

    register: function () {
        if (app.credential.get('loggedIn')) {
          this.navigate('#home', true);
          return;
        }

        // Since the home view never changes, we instantiate it and render it only once
        if (!app.registerView) {
            app.registerView = new app.RegisterView();
            app.registerView.render(null);
        } else {
            console.log('reusing register view');
            app.registerView.delegateEvents(); // delegate events when the view is recycled
        }
        this.$content.html(app.registerView.el);
    },

    login: function() {
        if (app.credential.get('loggedIn')) {
          this.navigate('#home', true);
          return;
        }

        if (!app.loginView) {
            app.loginView = new app.LoginView();
            app.loginView.render(null);
        } else {
            console.log("reusing login view");
            app.loginView.delegateEvents();
        }
        this.$content.html(app.loginView.el);
    },

    logout: function() {
      $.ajax({
            url:"/logout",
            type:'POST',
            dataType:"json",
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            success:function () {
              app.credential.setSessionId(null);
            }
        });
    }
});

$(document).on("ready", function () {
    app.loadTemplates(["ShellView", "RegisterView", "LoginView", "HomeView"],
        function () {
            app.router = new app.Router();
            Backbone.history.start();
        });
});
