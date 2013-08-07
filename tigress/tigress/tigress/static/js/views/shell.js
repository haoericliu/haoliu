app.ShellView = Backbone.View.extend({

  initialize: function () {
  },

  render: function () {
    this.$el.html(this.template({loggedIn: app.credential.get('loggedIn')}));
    return this;
  },

  events: {
    "keyup .search-query": "search",
    "keypress .search-query": "onkeypress"
  },

  selectMenuItem: function(menuItem) {
    $('.navbar .nav li').removeClass('active');
    if (menuItem) {
      $('.' + menuItem).addClass('active');
    }
  }
});
