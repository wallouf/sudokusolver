var dataURLToBlob = function(dataURL) {
    var BASE64_MARKER = ';base64,';
    if (dataURL.indexOf(BASE64_MARKER) == -1) {
      var parts = dataURL.split(',');
      var contentType = parts[0].split(':')[1];
      var raw = parts[1];

      return new Blob([raw], {type: contentType});
    }

    var parts = dataURL.split(BASE64_MARKER);
    var contentType = parts[0].split(':')[1];
    var raw = window.atob(parts[1]);
    var rawLength = raw.length;

    var uInt8Array = new Uint8Array(rawLength);

    for (var i = 0; i < rawLength; ++i) {
      uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], {type: contentType});
};

var uploadFile = function(file) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://f8hs96phw6.execute-api.eu-west-3.amazonaws.com/stage/solve');
    xhr.onload = function() {
        console.log(file.filename+' uploaded');
        handleComplete(file.size);
    };
    xhr.onerror = function() {
        console.log(this.responseText);
        handleComplete(file.size);
    };
    xhr.upload.onprogress = function(event) {
        handleProgress(event);
    }

    var formData = new FormData();
    formData.append('myfile', file);
    xhr.send(formData);
};

function resizeAndUploadFile(current_file){
  // var current_file = files[0];
  var reader = new FileReader();
  if (current_file.type.indexOf('image') == 0) {
    reader.onload = function (event) {
        var image = new Image();
        image.src = event.target.result;

        image.onload = function() {
          var maxWidth = 1024,
              maxHeight = 1024,
              imageWidth = image.width,
              imageHeight = image.height;


          if (imageWidth > imageHeight) {
            if (imageWidth > maxWidth) {
              imageHeight *= maxWidth / imageWidth;
              imageWidth = maxWidth;
            }
          }
          else {
            if (imageHeight > maxHeight) {
              imageWidth *= maxHeight / imageHeight;
              imageHeight = maxHeight;
            }
          }

          var canvas = document.createElement('canvas');
          canvas.width = imageWidth;
          canvas.height = imageHeight;
          image.width = imageWidth;
          image.height = imageHeight;
          var ctx = canvas.getContext("2d");
          ctx.drawImage(this, 0, 0, imageWidth, imageHeight);

          // Convert the resize image to a new file to post it.
          uploadFile(dataURLToBlob(canvas.toDataURL(current_file.type)));
        }
    }
    reader.readAsDataURL(current_file);
  }
}