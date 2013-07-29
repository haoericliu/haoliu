app.CategoryView = Backbone.View.extend({
  el: 'div',

  initialize: function(el) {
    this.categories = new app.Categories();
    this.rootel = el
    _.bindAll(this, "render");
    var that = this;
    this.categories.fetch({success: function() {
        that.render();
      }, error: function() {
        console.log("error");
      }
    });
  },

  render: function() {
    this.rootel.html(this.template({categories: this.categories.toJSON()}));

    return this;
  },
})




