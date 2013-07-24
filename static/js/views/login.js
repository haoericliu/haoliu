app.LoginView = Backbone.View.extend({

    events:{
        "submit #login-form":"submit"
    },

    render:function (data) {
        this.$el.html(this.template(data));
        return this;
    },

    submit:function (e) {
      e.preventDefault();
      
      var data = {
        "username": this.$("input[name=username]").val(),
        "password": this.$("input[name=password]").val(),
      }

      var login = new app.Login(data);
      var that = this;
      login.save(null, {
        success: function(model, response) {
          app.router.navigate("#", true); 
        },
        error: function(model, response) {
          that.render($.parseJSON(response.responseText));
        }
      });
    }

});
