app.HomeView = Backbone.View.extend({

    events:{
        "submit #signup-form":"submit"
    },

    render:function () {
        this.$el.html(this.template());
        return this;
    },

    submit:function (e) {
      e.preventDefault();
      
      var data = {
        "username": this.$("input[name=username]").val(),
        "password": this.$("input[name=password]").val(),
        "verify": this.$("input[name=verify]").val(),
        "email": this.$("input[name=email]").val()
      }

     var signup = new app.Signup(data);
     signup.save();
    }

});
