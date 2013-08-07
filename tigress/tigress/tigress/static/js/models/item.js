app.Photo = Backbone.Model.extend({

  urlRoot:"/photo",
  
  initialize:function () {
  }

});

app.Photos = Backbone.Collection.extend({
  url:"/photos",
  model: app.Photo,
  parse : function(data) {
    return data.data;
  }
});
