app.Category = Backbone.Model.extend({

  urlRoot:"/category",
  
  initialize:function () {
  }

});

app.Categories = Backbone.Collection.extend({
  url:"/category/all",
  model: app.Category,
  parse : function(data) {
    return data.data;
  }
});
