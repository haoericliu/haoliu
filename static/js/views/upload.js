app.UploadView= Backbone.View.extend({

    events:{
      "change #imageLoader": "handleImage",
      "click #imageSubmit": "submitImage"
    },

    render:function (data) {
        this.$el.html(this.template(data));
        this.canvas = this.$('#imageCanvas').get(0);
        this.ctx = this.canvas.getContext('2d');
        return this;
    },

    handleImage: function(e) {
      var reader = new FileReader();
      var that = this;
      reader.onload = function(event){
        var img = new Image();
        img.onload = function(){
          var MAX_WIDTH = 640;
          var MAX_HEIGHT = 480;
          var width = img.width;
          var height = img.height;

          if (width > height) {
            if (width > MAX_WIDTH) {
              height *= MAX_WIDTH / width;
              width = MAX_WIDTH;
            }
          } else {
            if (height > MAX_HEIGHT) {
              width *= MAX_HEIGHT / height;
              height = MAX_HEIGHT;
            }
          }
            that.canvas.width = width;
            that.canvas.height = height;
            that.ctx.drawImage(img,0,0, width, height);
            that.dataurl = that.canvas.toDataURL("image/jpeg");
        }
        img.src = event.target.result;
      }
      reader.readAsDataURL(e.target.files[0]);   
      that.file = e.target.files[0];
    },

    submitImage: function(e) {
      var formData = new FormData();
      formData.append('file', that.dataurl);
      //var xhr = new XMLHttpRequest();
      //xhr.open('POST', '/upload');
      //xhr.send(formData);
      $.ajax({
        type: "POST",
        url: "/upload",
        data: formData,
        contentType:false,
        processData:false,
      }).done(function(msg) {
        console.log(msg);
      }).fail(function(msg) { 
        console.log(msg);
      });
    }
});
