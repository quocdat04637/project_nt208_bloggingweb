$(document).ready(function () {
  var registrationSuccessful = $('#successModal').data('registration-successful');
  if (registrationSuccessful === 'true') {
    $('#successModal').modal('show');
  }
});


var slideIndex = 0;
showSlides();

function showSlides() {
    var i;
    var slides = document.getElementsByClassName("category-list-all");
    
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    
    slideIndex++;
    
    if (slideIndex > slides.length) { slideIndex = 1 }
    
    slides[slideIndex - 1].style.display = "block";
    setTimeout(showSlides, 2000); // Change slide every 2 seconds
}

function plusSlides(n) {
    slideIndex += n;
    var slides = document.getElementsByClassName("category-list-all");
    
    if (slideIndex > slides.length) { slideIndex = 1 }
    if (slideIndex < 1) { slideIndex = slides.length }
    
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    
    slides[slideIndex - 1].style.display = "block";
}


// Xử lý nút like
$(document).ready(function() {
  $('.like-button').click(function() {
      var commentId = $(this).data('comment');
      var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  // Lấy token CSRF từ biểu mẫu
      $.ajax({
          url: '/like_comment/' + commentId + '/',
          type: 'POST',
          data: {'csrfmiddlewaretoken': csrfToken},  // Gửi token CSRF trong dữ liệu POST
          dataType: 'json',
          success: function(response) {
              if (response.message === 'Liked successfully') {
                  // Cập nhật số lượt "like" trên trang
                  $('.likes-count[data-comment="' + commentId + '"]').text('Likes: ' + response.likes);
                  // Ẩn nút "Like"
                  $(this).hide();
              } else {
                  alert(response.message);
              }
          }
      });
  });
});


